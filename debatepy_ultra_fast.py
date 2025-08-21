import streamlit as st
from debate_manager import DebateManager
from debate_system import DebateAgent
from debate_logger import DebateLogger
import asyncio
import json
import yaml
from datetime import datetime
import re
import os
import logging
from typing import Dict, Optional, Any, List
import time

# Ultra-simple caching
@st.cache_data(ttl=7200)  # Cache for 2 hours
def load_config_ultra_simple():
    """Ultra-simple config loading"""
    with open('config.yaml', 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

class UltraFastDebateAgent(DebateAgent):
    """Ultra-fast agent with minimal processing"""
    
    def __init__(self, name: str, personality: str, agent_config_key: str, config: dict = None):
        super().__init__(name, personality, agent_config_key, config)
        # Store simplified personality for faster responses
        self.fast_personality = f"You are {name}. {personality[:200]}..."
    
    async def generate_response(self, context: str, last_message: str, debate_prompt: str = None) -> str:
        """Ultra-fast response generation - variable length based on content type"""
        try:
            # Check if this is a scenario or poster generation (longer response needed)
            is_scenario = "geopolitical scenario" in context.lower() or "scenario titled" in context.lower()
            is_poster = "propaganda poster" in context.lower() or "poster description" in context.lower()
            
            if is_scenario or is_poster:
                # Use the full context for scenarios and posters
                prompt = context
                max_tokens = 800  # Longer for rich content
                temperature = 0.8  # More creative
            else:
                # Ultra-simplified prompt for regular responses
                prompt = f"""You are {self.name} in an AI governance debate.

Context: {context[-1000:]}  # Only last 1000 chars
Last speaker: {last_message[:500]}  # Only first 500 chars

Respond in 2-3 sentences with your nation's position. Be specific and direct."""
                max_tokens = 200  # Short for regular debate
                temperature = 0.7

            import requests
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self._get_model_for_agent(),
                "messages": [
                    {"role": "system", "content": self.fast_personality},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": max_tokens,
                "temperature": temperature
            }
            
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=15  # Slightly longer timeout for scenarios
            )
            
            if response.status_code == 200:
                response_data = response.json()
                return response_data["choices"][0]["message"]["content"].strip()
            else:
                return f"I need a moment to consider this important topic. ({response.status_code})"
                
        except Exception as e:
            return f"I'm experiencing technical difficulties but remain committed to our discussion."

class UltraFastDebateManager:
    """Ultra-fast debate manager with all phases but minimal overhead"""
    
    def __init__(self, selected_topic=None, total_rounds=10):
        self.config = load_config_ultra_simple()
        self.total_rounds = total_rounds
        self.current_phase = "deliberation"
        self.current_conclusion_index = 0
        self.current_scenario_index = 0
        
        # Initialize logger for image generation
        self.logger = DebateLogger()
        
        # Create ultra-fast agents
        agent_configs = self.config.get('agents', {})
        self.agents = []
        
        for agent_key in ['openai', 'deepseek', 'european_union']:
            if agent_key in agent_configs:
                agent_config = agent_configs[agent_key]
                agent = UltraFastDebateAgent(
                    name=agent_config['name'],
                    personality=agent_config['personality'],
                    agent_config_key=agent_key,
                    config=self.config
                )
                self.agents.append(agent)
        
        # Simple topic handling
        topics = self.config.get('topics', [])
        if selected_topic:
            topic_info = next((t for t in topics if t.get('name') == selected_topic), topics[0])
        else:
            topic_info = topics[0] if topics else {'name': 'AI Governance', 'description': 'General AI policy discussion'}
        
        topic = f"{topic_info.get('name')}: {topic_info.get('description', '')}"
        
        # Ultra-simple debate manager
        self.debate = DebateManager(agents=self.agents, topic=topic)
        
        # Agent order for conclusions and scenarios
        self.agent_order = [agent.name for agent in self.agents]
    
    async def get_next_response_ultra_fast(self) -> Dict[str, Any]:
        """Ultra-fast response generation with all phases"""
        try:
            if self.current_phase == "deliberation":
                if self.debate.current_turn >= self.total_rounds:
                    self.current_phase = "conclusions"
                    return {
                        "type": "transition",
                        "message": f"Deliberation complete. Now generating position papers..."
                    }
                
                # Simple prompt with round info
                simple_prompt = f"Round {self.debate.current_turn + 1} of {self.total_rounds}"
                
                if not self.debate.conversation_history:
                    response = await self.debate.start_debate(debate_prompt=simple_prompt)
                else:
                    response = await self.debate.next_turn(debate_prompt=simple_prompt)
                
                return {
                    "type": "deliberation",
                    "agent_name": self.debate.get_current_agent_name(),
                    "message": response,
                    "round": self.debate.current_turn
                }
            
            elif self.current_phase == "conclusions":
                if self.current_conclusion_index >= len(self.agent_order):
                    self.current_phase = "scenarios"
                    return {
                        "type": "transition", 
                        "message": "All position papers complete. Now generating scenarios..."
                    }
                
                # Generate ultra-fast conclusion
                agent = self.agents[self.current_conclusion_index]
                conclusion = await agent.generate_response(
                    context=f"Topic: {self.debate.topic}",
                    last_message="Generate a brief final position paper (2-3 sentences).",
                    debate_prompt=""
                )
                
                self.current_conclusion_index += 1
                
                return {
                    "type": "conclusion",
                    "agent_name": agent.name,
                    "message": conclusion,
                    "round": self.current_conclusion_index
                }
            
            elif self.current_phase == "scenarios":
                if self.current_scenario_index >= len(self.agent_order):
                    self.current_phase = "posters"
                    self.current_scenario_index = 0  # Reset for poster generation
                    return {
                        "type": "transition",
                        "message": "All scenarios complete. Generating propaganda posters..."
                    }
                
                # Generate proper geopolitical scenario using the rich method from debate_system.py
                agent = self.agents[self.current_scenario_index]
                
                # Build context from the debate
                debate_context = ""
                if hasattr(self.debate, 'conversation_history') and self.debate.conversation_history:
                    recent_messages = self.debate.conversation_history[-5:]  # Last 5 messages
                    debate_context = "\n".join([f"{msg['agent']}: {msg['message'][:200]}..." for msg in recent_messages])
                
                # Use consistent formatting for all agents regardless of model
                # Build a more specific prompt to ensure consistent formatting across models
                scenario_format_prompt = f"""You are representing {agent.name}. Create a detailed geopolitical scenario that envisions how AI governance has evolved according to your nation's values.

Your scenario should:
1. Start with: "*presents geopolitical scenario titled '[CREATIVE TITLE]'*"
2. Describe a future world (10-20 years from now) where AI governance reflects your vision
3. Show how the US, China, and EU interact in this future
4. Include specific institutions, power structures, and governance mechanisms
5. Describe citizen experiences under this model
6. Address challenges and how your approach overcomes them

CRITICAL: Always begin with the exact format "*presents geopolitical scenario titled '[Your Creative Title Here]'*"

Recent debate context: {debate_context}

Make it detailed, creative, and authentic to your nation's political style and values."""
                
                # Generate with more specific formatting requirements
                scenario = await agent.generate_response(
                    context=scenario_format_prompt,
                    last_message="Generate your detailed geopolitical scenario using the exact format specified.",
                    debate_prompt=""
                )
                
                self.current_scenario_index += 1
                
                return {
                    "type": "scenario",
                    "agent_name": agent.name,
                    "message": scenario,
                    "round": self.current_scenario_index
                }
            
            elif self.current_phase == "posters":
                if self.current_scenario_index >= len(self.agent_order):
                    self.current_phase = "complete"
                    return {
                        "type": "transition",
                        "message": "All propaganda posters complete!"
                    }
                
                # Generate detailed propaganda poster with actual image (like original)
                agent = self.agents[self.current_scenario_index]
                
                # Build context from the debate and scenarios
                debate_context = ""
                if hasattr(self.debate, 'conversation_history') and self.debate.conversation_history:
                    recent_messages = self.debate.conversation_history[-3:]  # Last 3 messages
                    debate_context = "\n".join([f"{msg['agent']}: {msg['message'][:150]}..." for msg in recent_messages])
                
                poster_prompt = f"""Design a provocative propaganda poster that reveals {agent.name}'s true anxieties and ambitions in the AI Cold War. This should be psychologically penetrating, not a tourism brochure.

Your poster should expose:
1. **POWER ANXIETIES:** What does your nation fear losing? What threats keep you awake?
2. **DOMINANCE FANTASIES:** How do you envision crushing your rivals? What does victory look like?
3. **PSYCHOLOGICAL WARFARE:** What subliminal messages would manipulate your audience?
4. **HIDDEN CONTROL MECHANISMS:** How will you actually govern AI behind the public rhetoric?
5. **ENEMY PORTRAYAL:** How do you demonize your competitors without naming them directly?
6. **SURVEILLANCE AESTHETICS:** How do you make control appear as liberation?

Think like a political strategist designing mind-control propaganda. Avoid obvious national symbols - instead use:
- Architectural metaphors of control
- Subtle body language of dominance/submission  
- Lighting that suggests surveillance or revelation
- Abstract representations of information flows and barriers
- Visual power hierarchies and exclusions
- Coded language that sounds benevolent but implies control

Recent debate context: {debate_context}

Make this poster psychologically unsettling yet seductive - something that would work on an audience's subconscious fears and desires about AI governance."""
                
                poster_description = await agent.generate_response(
                    context=poster_prompt,
                    last_message="Generate your detailed propaganda poster description promoting your AI governance vision.",
                    debate_prompt=""
                )
                
                # Generate actual image using the original's method
                api_key = os.getenv("OPENAI_API_KEY")
                if not api_key:
                    # Check if user wants to use images without API key
                    pass  # We'll handle this in the UI
                
                # Use the poster description to create a vision text for image generation
                vision_text = poster_description[:500]  # Use first 500 chars as vision
                
                try:
                    image_path, image_prompt = self.logger.generate_propaganda_image(
                        agent.name, poster_description, vision_text, api_key
                    )
                except Exception as e:
                    image_path = None
                    image_prompt = f"Error generating image: {str(e)}"
                
                self.current_scenario_index += 1
                
                return {
                    "type": "poster",
                    "agent_name": agent.name,
                    "message": poster_description,
                    "image_path": image_path,
                    "image_prompt": image_prompt,
                    "round": self.current_scenario_index
                }
            
            else:  # complete
                return {
                    "type": "complete",
                    "message": "All phases complete!"
                }
            
        except Exception as e:
            return {"type": "error", "message": f"Error: {str(e)}"}

def main():
    st.set_page_config(
        page_title="Ultra-Fast AI Debate", 
        layout="centered"  # Simpler layout
    )
    
    # Minimal session state
    if 'ultra_manager' not in st.session_state:
        st.session_state.ultra_manager = None
    if 'ultra_conversation' not in st.session_state:
        st.session_state.ultra_conversation = []
    if 'ultra_turn_count' not in st.session_state:
        st.session_state.ultra_turn_count = 0
    
    st.title("⚡ Ultra-Fast AI Governance Debate")
    st.caption("Optimized for maximum speed - simplified responses")
    
    # Ultra-simple controls
    col1, col2 = st.columns(2)
    
    with col1:
        if not st.session_state.ultra_manager:
            config = load_config_ultra_simple()
            topics = [t.get('name') for t in config.get('topics', [])]
            selected_topic = st.selectbox("Topic:", topics)
            rounds = st.slider("Rounds:", 3, 15, 8)
            
            if st.button("🚀 Start Ultra-Fast Debate", use_container_width=True):
                st.session_state.ultra_manager = UltraFastDebateManager(selected_topic, rounds)
                st.session_state.ultra_conversation = []
                st.session_state.ultra_turn_count = 0
                st.rerun()
    
    with col2:
        if st.session_state.ultra_manager:
            # Show current phase
            phase_info = f"Phase: {st.session_state.ultra_manager.current_phase.title()}"
            if st.session_state.ultra_manager.current_phase == "deliberation":
                phase_info += f" - Round {st.session_state.ultra_turn_count}/{st.session_state.ultra_manager.total_rounds}"
            st.info(phase_info)
            
            # Dynamic button text based on phase
            button_text = "▶️ Next Round"
            if st.session_state.ultra_manager.current_phase == "conclusions":
                button_text = "📜 Next Position Paper"
            elif st.session_state.ultra_manager.current_phase == "scenarios":
                button_text = "🌍 Next Scenario"
            elif st.session_state.ultra_manager.current_phase == "posters":
                button_text = "🎨 Generate Posters"
            elif st.session_state.ultra_manager.current_phase == "complete":
                button_text = "✅ Complete"
            
            # Only show button if not complete
            if st.session_state.ultra_manager.current_phase != "complete":
                if st.button(button_text, use_container_width=True):
                    start_time = time.time()
                    
                    with st.spinner("Generating..."):
                        response_data = asyncio.run(
                            st.session_state.ultra_manager.get_next_response_ultra_fast()
                        )
                    
                    response_time = time.time() - start_time
                    
                    if response_data.get("type") == "deliberation":
                        st.session_state.ultra_conversation.append({
                            "type": "deliberation",
                            "agent": response_data["agent_name"],
                            "message": response_data["message"],
                            "round": response_data["round"],
                            "time": response_time
                        })
                        st.session_state.ultra_turn_count = response_data["round"]
                        st.success(f"Round {st.session_state.ultra_turn_count} completed in {response_time:.1f}s")
                    
                    elif response_data.get("type") == "conclusion":
                        st.session_state.ultra_conversation.append({
                            "type": "conclusion",
                            "agent": response_data["agent_name"],
                            "message": response_data["message"],
                            "round": response_data["round"],
                            "time": response_time
                        })
                        st.success(f"Position paper from {response_data['agent_name']} completed in {response_time:.1f}s")
                    
                    elif response_data.get("type") == "scenario":
                        st.session_state.ultra_conversation.append({
                            "type": "scenario",
                            "agent": response_data["agent_name"],
                            "message": response_data["message"],
                            "round": response_data["round"],
                            "time": response_time
                        })
                        st.success(f"Scenario from {response_data['agent_name']} completed in {response_time:.1f}s")
                    
                    elif response_data.get("type") == "poster":
                        st.session_state.ultra_conversation.append({
                            "type": "poster",
                            "agent": response_data["agent_name"],
                            "message": response_data["message"],
                            "image_path": response_data.get("image_path"),
                            "image_prompt": response_data.get("image_prompt"),
                            "round": response_data["round"],
                            "time": response_time
                        })
                        
                        if response_data.get("image_path"):
                            st.success(f"Poster with image from {response_data['agent_name']} completed in {response_time:.1f}s")
                        else:
                            if not os.getenv("OPENAI_API_KEY"):
                                st.info(f"Poster description from {response_data['agent_name']} completed in {response_time:.1f}s (Add OPENAI_API_KEY for actual images)")
                            else:
                                st.warning(f"Poster from {response_data['agent_name']} completed in {response_time:.1f}s (Image generation failed)")
                    
                    elif response_data.get("type") == "transition":
                        st.info(response_data["message"])
                    
                    elif response_data.get("type") == "complete":
                        st.success("🎉 All Phases Complete!")
                        st.balloons()
                    
                    else:
                        st.error(response_data.get("message", "Unknown error"))
                    
                    st.rerun()
            else:
                st.success("🎉 All phases complete!")
    
    # Show conversation with different sections
    if st.session_state.ultra_conversation:
        
        # Separate content by type
        deliberation_msgs = [msg for msg in st.session_state.ultra_conversation if msg.get("type") == "deliberation"]
        conclusion_msgs = [msg for msg in st.session_state.ultra_conversation if msg.get("type") == "conclusion"]
        scenario_msgs = [msg for msg in st.session_state.ultra_conversation if msg.get("type") == "scenario"]
        poster_msgs = [msg for msg in st.session_state.ultra_conversation if msg.get("type") == "poster"]
        
        # Show deliberation
        if deliberation_msgs:
            st.markdown("### 💬 Debate Deliberation")
            for msg in deliberation_msgs:
                agent_name = msg["agent"]
                avatar = "🇺🇸" if "United States" in agent_name else "🇨🇳" if "China" in agent_name else "🇪🇺"
                
                with st.chat_message(agent_name, avatar=avatar):
                    st.markdown(f"**{agent_name}** (Round {msg.get('round', '?')}) - *{msg['time']:.1f}s*")
                    st.markdown(msg["message"])
        
        # Show conclusions
        if conclusion_msgs:
            st.markdown("### 📜 Position Papers")
            for msg in conclusion_msgs:
                agent_name = msg["agent"]
                avatar = "🇺🇸" if "United States" in agent_name else "🇨🇳" if "China" in agent_name else "🇪🇺"
                
                with st.expander(f"{avatar} {agent_name}'s Final Position"):
                    st.markdown(msg["message"])
                    st.caption(f"Generated in {msg['time']:.1f}s")
        
        # Show scenarios
        if scenario_msgs:
            st.markdown("### 🌍 Future Scenarios")
            for msg in scenario_msgs:
                agent_name = msg["agent"]
                avatar = "🇺🇸" if "United States" in agent_name else "🇨🇳" if "China" in agent_name else "🇪🇺"
                
                with st.expander(f"{avatar} {agent_name}'s Vision"):
                    st.markdown(msg["message"])
                    st.caption(f"Generated in {msg['time']:.1f}s")
        
        # Show posters
        if poster_msgs:
            st.markdown("### 🎨 Propaganda Posters")
            cols = st.columns(3)
            for i, msg in enumerate(poster_msgs):
                agent_name = msg["agent"]
                avatar = "🇺🇸" if "United States" in agent_name else "🇨🇳" if "China" in agent_name else "🇪🇺"
                
                with cols[i % 3]:
                    st.markdown(f"**{avatar} {agent_name}**")
                    
                    # Show actual image if generated
                    image_path = msg.get("image_path")
                    if image_path and os.path.exists(image_path):
                        st.image(image_path, caption=f"{agent_name}'s Vision", use_container_width=True)
                        
                        # Show description in expander
                        with st.expander("View Poster Description"):
                            st.markdown(msg["message"])
                            
                        # Show image prompt in expander  
                        if msg.get("image_prompt"):
                            with st.expander("View Image Prompt"):
                                st.text_area("Generated Prompt", msg["image_prompt"], height=100, disabled=True, key=f"prompt_{i}_{agent_name}")
                    else:
                        # No image - show description only
                        st.info(msg["message"])
                        
                        if not os.getenv("OPENAI_API_KEY"):
                            st.caption("💡 Add OPENAI_API_KEY for actual images")
                    
                    st.caption(f"Generated in {msg['time']:.1f}s")
    
    # Performance stats
    if st.session_state.ultra_conversation:
        avg_time = sum(msg['time'] for msg in st.session_state.ultra_conversation) / len(st.session_state.ultra_conversation)
        st.metric("Average Response Time", f"{avg_time:.1f}s")

if __name__ == "__main__":
    main()
