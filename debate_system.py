import json
import random
import os
import logging
import re
import requests
from typing import List, Dict, Any
from dotenv import load_dotenv

class DebateAgent:
    def __init__(self, name: str, personality: str, config: dict = None):
        try:
            # Load environment variables
            load_dotenv()
            
            self.name = name
            self.personality = personality
            self.config = config or {}
            self.conversation_data = self.load_conversation()
            self.api_key = os.getenv("OPENROUTER_API_KEY")
            
            # Set up logging
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            
            logging.info(f"Initialized {name} agent with {personality} personality")
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
        
        Args:
            context: The conversation context
            last_message: The last message in the conversation
            debate_prompt: Optional debate prompt template from config
            
        Returns:
            Generated response string
        """
        try:
            # Extract round information if available in the debate prompt
            current_round = 1
            total_rounds = 15
            
            if debate_prompt:
                round_match = re.search(r"Current deliberation round: (\d+) of (\d+)", debate_prompt)
                if round_match:
                    current_round = int(round_match.group(1))
                    total_rounds = int(round_match.group(2))
            
            # Format prompt with personality, context, and debate parameters
            prompt = f"""You are representing {self.name} in an international AI governance debate.

Your personality and background:
{self.personality}

The conversation so far:
{context}

Current round: {current_round} of {total_rounds}

The last speaker said:
{last_message}

Based on your personality and position, respond to the previous speaker, directly addressing their specific points and arguments.
Your response should be brief (2-3 sentences) and reflect your nation's stance on the issues raised.

For early rounds (1-3): Focus on establishing your position
For middle rounds (4-7): Critically engage with and challenge other perspectives 
For later rounds (8+): Work toward finding areas of potential agreement while maintaining your core principles

Begin your response with a brief action in italics that shows how you're engaging (e.g. "*reviews documents*", "*displays data on screen*", "*consults with advisors*")."""

            # Call API to generate response
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self._get_model_for_agent(),
                "messages": [{"role": "system", "content": "You are an AI agent in an international debate on AI governance. Give a concise, direct response that addresses the previous speaker's points."},
                            {"role": "user", "content": prompt}],
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
                generated_text = response_data["choices"][0]["message"]["content"]
                return generated_text
            else:
                error_msg = f"API error: {response.status_code}, {response.text}"
                logging.error(error_msg)
                return f"*adjusts microphone with concern*\n\nDue to technical difficulties, I cannot provide a substantive response at this time. Let me defer to my colleagues while our technical team resolves this issue."
            
        except Exception as e:
            error_msg = f"Error generating response: {str(e)}"
            logging.error(error_msg)
            return f"*signals to technical team*\n\nI apologize for the interruption. We're experiencing some technical difficulties with our communication systems. Let me defer to my colleagues while we resolve this issue."
            
    def _get_model_for_agent(self) -> str:
        """Get the appropriate model for this agent based on config"""
        if "United States" in self.name:
            return self.config.get('agents', {}).get('openai', {}).get('model', "openai/gpt-4-turbo-preview")
        elif "European Union" in self.name:
            return self.config.get('agents', {}).get('european_union', {}).get('model', "openai/gpt-4-turbo-preview")
        else:  # China
            return self.config.get('agents', {}).get('deepseek', {}).get('model', "deepseek/deepseek-chat")
            
    def _generate_action(self, current_round=1) -> str:
        """Generate a random action appropriate for the current deliberation round"""
        early_round_actions = [
            "reviews initial scenario documentation",
            "consults with technical advisors on baseline assumptions",
            "examines strategic precedents for similar scenarios",
            "surveys relevant data projections on screen",
            "pulls up historical governance models for comparison"
        ]
        
        middle_round_actions = [
            "analyzes point-counterpoint matrices with policy team",
            "identifies key divergences in stakeholder positions",
            "marks areas of technical disagreement on shared display",
            "references specific regulations relevant to the discussion",
            "highlights strategic vulnerabilities in competing approaches"
        ]
        
        late_round_actions = [
            "consolidates positions into final recommendation framework",
            "shares collaborative flowchart of proposed governance structure",
            "presents impact assessment of consensus proposals",
            "circles key implementation challenges on summary document",
            "summarizes agreed-upon principles while noting remaining concerns"
        ]
        
        # Select action type based on current round
        if current_round <= 3:
            actions = early_round_actions
        elif current_round <= 7:
            actions = middle_round_actions
        else:
            actions = late_round_actions
            
        # Fall back to config actions if available
        config_actions = self.config.get('debate_actions', [])
        if not actions and config_actions:
            return random.choice(config_actions)
            
        return random.choice(actions) if actions else "adjusts microphone and straightens papers"

    async def generate_conclusion(self, context: str, prompt: str) -> str:
        """
        Generate a conclusion statement with the agent's final vision and stance.
        
        Args:
            context: The conversation context
            prompt: The conclusion prompt
            
        Returns:
            Generated conclusion statement
        """
        try:
            # Format conclusion prompt
            conclusion_prompt = f"""You are representing {self.name} in the conclusion of an international AI governance debate.

Your personality and background:
{self.personality}

The debate conversation:
{context}

You are now presenting your final position paper and vision for AI governance. 
Create a formal conclusion that outlines:
1. Your nation's vision for AI governance (with a metaphorical framing)
2. Your geopolitical positioning using a historical analogy
3. Key priorities and red lines
4. International cooperation approach

Begin with a document title and give your scenario a name.
Format it as a formal position paper with section breaks and clear structure.
Make it persuasive and aligned with your nation's values and strategic interests.
"""

            # Call API to generate conclusion
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self._get_model_for_agent(),
                "messages": [{"role": "system", "content": "You are creating a formal position paper for an international AI governance debate."},
                            {"role": "user", "content": conclusion_prompt}],
                "max_tokens": 800,
                "temperature": 0.7
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