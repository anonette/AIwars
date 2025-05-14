import json
import random
import os
import logging
import re
import requests
import asyncio # Added for async _generate_action
from typing import List, Dict, Any
from dotenv import load_dotenv

# Define a default model in case lookup fails
DEFAULT_MODEL = "openai/gpt-3.5-turbo" 

class DebateAgent:
    def __init__(self, name: str, personality: str, agent_config_key: str, config: dict = None):
        try:
            # Load environment variables
            load_dotenv()
            
            self.name = name
            self.personality = personality
            self.agent_config_key = agent_config_key # Store the key for model lookup
            self.config = config or {} # This is the overall config from config.yaml
            self.conversation_data = self.load_conversation()
            self.api_key = os.getenv("OPENROUTER_API_KEY")
            
            # Set up logging
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            
            logging.info(f"Initialized {name} agent with {personality} personality, using config key '{agent_config_key}'")
        except Exception as e:
            logging.error(f"Error initializing DebateAgent: {str(e)}")
            raise
        
    def load_conversation(self, filename='debate_conversation.json') -> List[Dict[str, Any]]:
        """
        Load conversation history from a JSON file, filtering for this agent's messages.
        
        Args:
            filename: Path to the conversation JSON file
            
        Returns:
            List of message dictionaries for this agent
        """
        if not os.path.exists(filename):
            logging.warning(f"Conversation file {filename} not found")
            return []
            
        try:
            # Open file with UTF-8 encoding
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [msg for msg in data if msg.get('agent') == self.name]
        except UnicodeDecodeError:
            # Fallback to different encoding if UTF-8 fails
            logging.warning(f"UTF-8 decode error, trying UTF-8-SIG encoding")
            with open(filename, 'r', encoding='utf-8-sig') as f:
                data = json.load(f)
                return [msg for msg in data if msg.get('agent') == self.name]
        except json.JSONDecodeError as e:
            logging.error(f"JSON decode error: {str(e)}")
            return []
        except Exception as e:
            logging.error(f"Error loading conversation: {str(e)}")
            return []
        
    async def generate_response(self, context: str, last_message: str, debate_prompt: str = None) -> str:
        """
        Generate a response based on the conversation context and last message.
        Includes an LLM-generated action phrase.
        """
        try:
            current_round = 1
            total_rounds = 15 # Default, consider making this more dynamic if needed
            if debate_prompt:
                round_match = re.search(r"Current deliberation round: (\d+) of (\d+)", debate_prompt)
                if round_match:
                    current_round = int(round_match.group(1))
                    total_rounds = int(round_match.group(2))

            # Generate action phrase using LLM
            action_phrase = await self._generate_action(current_round, last_message)
            
            # Format prompt for dialogue, informing the LLM of the action taken.
            dialogue_prompt = f"""You are representing {self.name} in an international AI governance debate.

Your personality and background:
{self.personality}

The conversation so far (avoid repeating points made here unless you are directly building upon them with a new insight):
{context}

Current round: {current_round} of {total_rounds}.

The last speaker ({last_message.split(':')[0].strip() if ':' in last_message else 'Previous Speaker'}) said:
"{last_message.split(':', 1)[-1].strip() if ':' in last_message else last_message}"

You have just performed the action: *{action_phrase}*

Now, provide your spoken response. Your response must:
1. Be brief (2-3 impactful sentences).
2. Directly address specific points from the last speaker.
3. Reflect your nation's unique stance and strategic interests.
4. CRITICAL: Avoid repeating arguments you or others have already made. Introduce new perspectives, deepen existing arguments with fresh details, or identify new connections.

Debate Stage Guidance:
- Early rounds (1-3 of {total_rounds}): Clearly establish your core principles and initial position on the topic.
- Middle rounds (4-{total_rounds - max(3, total_rounds // 3)} of {total_rounds}): Critically engage with others. Challenge assumptions, introduce counter-arguments, and highlight the nuances or potential flaws in opposing views. Evolve your arguments based on the discussion.
- Later rounds ({(total_rounds - max(3, total_rounds // 3)) + 1}-{total_rounds} of {total_rounds}): Focus on synthesis. Identify areas of potential convergence or irreducible disagreement. Propose constructive next steps or articulate conditions for cooperation, always maintaining your core national interests.

Deliver only your spoken dialogue. Do NOT include any action phrase in your response.
"""

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self._get_model_for_agent(), 
                "messages": [{"role": "system", "content": "You are an AI agent in an international debate on AI governance. Provide only the spoken dialogue as your response, following the user's instructions for content and tone."},
                            {"role": "user", "content": dialogue_prompt}],
                "max_tokens": 150,
                "temperature": 0.7
            }
            
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                response_data = response.json()
                generated_dialogue = response_data["choices"][0]["message"]["content"].strip()
                # Combine the LLM-generated action with the LLM-generated dialogue
                return f"*{action_phrase}*\n\n{generated_dialogue}"
            else:
                error_msg = f"API error in dialogue generation: {response.status_code}, {response.text}"
                logging.error(error_msg)
                # Fallback with a generic action if dialogue generation fails
                return f"*{action_phrase}*\n\nDue to technical difficulties, I cannot provide a substantive response at this time. Let me defer to my colleagues."
            
        except Exception as e:
            error_msg = f"Error generating response: {str(e)}"
            logging.error(error_msg)
            # Fallback with a generic action if any other error occurs
            return f"*signals to technical team with a concerned look*\n\nI apologize for the interruption. We're experiencing some technical difficulties. Let me defer to my colleagues."
            
    def _get_model_for_agent(self) -> str:
        """Get the appropriate model for this agent based on its agent_config_key and the overall config."""
        try:
            agent_specific_config = self.config.get('agents', {}).get(self.agent_config_key, {})
            model = agent_specific_config.get('model')
            if model:
                logging.info(f"Agent {self.name} (config key: {self.agent_config_key}) using model: {model}")
                return model
            else:
                logging.warning(f"Model not found for agent {self.name} (config key: {self.agent_config_key}). Using default model: {DEFAULT_MODEL}")
                return DEFAULT_MODEL
        except Exception as e:
            logging.error(f"Error getting model for agent {self.name}: {str(e)}. Using default model: {DEFAULT_MODEL}")
            return DEFAULT_MODEL
            
    async def _generate_action(self, current_round: int, last_message: str) -> str:
        """Generate an LLM-based action phrase suitable for the agent and debate stage."""
        try:
            round_stage = "early"
            if current_round > 7:
                round_stage = "late"
            elif current_round > 3:
                round_stage = "middle"

            action_prompt = f"""You are an AI debate agent representing {self.name}.
Your personality: {self.personality}
Debate stage: {round_stage} rounds (current round {current_round}).
The last speaker said: "{last_message[:150]}..." 

Generate a very brief, fitting, non-verbal action phrase for your agent to perform before speaking. 
Examples: 'reviews notes briefly', 'sips water thoughtfully', 'glances at advisors', 'nods in understanding', 'adjusts spectacles', 'leans forward intently'.
Do NOT use italics or quotation marks. Output only the action phrase itself. Max 5 words.
"""
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": self._get_model_for_agent(), # Or a smaller, faster model if preferred for actions
                "messages": [{"role": "system", "content": "You generate brief, non-verbal action phrases for a debate agent."}, 
                             {"role": "user", "content": action_prompt}],
                "max_tokens": 15, # Short response for an action
                "temperature": 0.6 # Slightly lower temperature for more predictable actions
            }

            # Using httpx for async request, or adapt if requests can be used with asyncio loop
            # For simplicity, sticking to synchronous requests here, assuming it's handled by asyncio.run elsewhere
            # If truly async execution is needed here, httpx or aiohttp would be better.
            # However, OpenRouter API calls are I/O bound, so running them in an executor with asyncio.to_thread
            # if called from an async context is also an option if sticking with the `requests` library.
            # For now, let's assume the calling context (like Streamlit) handles the async nature or this runs acceptably.
            
            # Simulating async behavior for now as `requests` is synchronous.
            # In a true async setup, you'd use an async HTTP client like httpx or aiohttp.
            # loop = asyncio.get_event_loop()
            # response = await loop.run_in_executor(None, lambda: requests.post(
            #     "https://openrouter.ai/api/v1/chat/completions",
            #     headers=headers,
            #     json=data
            # ))
            # This is a placeholder for a proper async http call if needed.
            # For now, making it a blocking call as `generate_response` is already async
            # and will be run within asyncio.run() by Streamlit or the calling framework.
            
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data
            )

            if response.status_code == 200:
                response_data = response.json()
                action = response_data["choices"][0]["message"]["content"].strip()
                # Further clean up if necessary (e.g., remove quotes if LLM adds them)
                action = action.replace('"', '').replace("'", "")
                logging.info(f"Agent {self.name} generated action: {action}")
                return action if action else "takes a moment to consider"
            else:
                logging.warning(f"API error generating action for {self.name}: {response.status_code}. Using fallback.")
                return "reviews notes" # Fallback action

        except Exception as e:
            logging.error(f"Error generating action for {self.name}: {str(e)}. Using fallback.")
            return "looks thoughtful" # Fallback action

    async def generate_conclusion(self, context: str) -> str:
        """
        Generate a conclusion statement with the agent's final vision and stance.
        
        Args:
            context: The conversation context (debate history)
            
        Returns:
            Generated conclusion statement
        """
        try:
            # Format conclusion prompt
            conclusion_prompt_text = f"""You are representing {self.name} in the conclusion of an international AI governance debate.

Your personality and background:
{self.personality}

The debate conversation so far:
{context}

You are now presenting your final position paper and vision for AI governance. 
Create a formal conclusion that outlines:
1. Your nation's vision for AI governance (with a metaphorical framing, e.g., 'Digital Frontier', 'Harmonious Garden', 'Regulated Agora')
2. Your geopolitical positioning using a historical or philosophical analogy (e.g., 'like the Renaissance city-states', 'akin to post-war global rebuilding efforts')
3. Key priorities and non-negotiable red lines for your nation.
4. Your approach to international cooperation on AI.

Begin your presentation with a phrase like "*unfurls a scroll labelled '{{DOCUMENT_TITLE}}'*" or "*projects a slide titled '{{SCENARIO_NAME}}'*" where {{DOCUMENT_TITLE}} or {{SCENARIO_NAME}} is a fitting, creative name you devise for your position paper or vision (e.g., 'The Digital Silk Road Compact', 'Blueprint for a Federated Algorithmic Order', 'Charter for Human-Centric AI').

Format your entire response as a formal position paper. It should be well-structured, persuasive, and clearly aligned with your nation's established values and strategic interests demonstrated throughout the debate.
Ensure the statement is comprehensive and serves as a definitive concluding summary of your stance."""

            # Call API to generate conclusion
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self._get_model_for_agent(),
                "messages": [{"role": "system", "content": "You are an expert diplomat and strategist creating a formal, comprehensive position paper for the conclusion of an international AI governance debate."},
                            {"role": "user", "content": conclusion_prompt_text}],
                "max_tokens": 1000, # Increased max_tokens for a more comprehensive conclusion
                "temperature": 0.75 # Slightly increased temperature for more creative/varied conclusions
            }
            
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                response_data = response.json()
                generated_conclusion = response_data["choices"][0]["message"]["content"]
                return generated_conclusion
            else:
                error_msg = f"API error in conclusion generation: {response.status_code}, {response.text}"
                logging.error(error_msg)
                
                # Fallback minimal conclusion in case of API failure
                if "United States" in self.name:
                    title = "The Innovation Archipelago"
                    document = "The Digital Frontiersman"
                elif "European Union" in self.name:
                    title = "The Balanced Integration Scenario"
                    document = "The Digital Agora"
                else:  # China
                    title = "The Ordered Prosperity Scenario"
                    document = "The Harmonious Cultivation"
                
                return f"""*presents "{document}" position paper*\n\n**{title}**\n\nDue to technical difficulties, I can only present a summary of our position. We remain committed to our core principles of governance while respecting the international deliberative process. Thank you for your understanding."""
                
        except Exception as e:
            error_msg = f"Error generating conclusion: {str(e)}"
            logging.error(error_msg)
            return f"*apologizes for technical difficulties*\n\nI regret that due to unforeseen technical issues, I cannot present our full position paper at this time. We look forward to sharing our comprehensive vision in follow-up communications." 