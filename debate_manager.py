from typing import List, Dict, Optional
from debate_system import DebateAgent
import asyncio
from datetime import datetime
import logging
from debate_logger import DebateLogger

class DebateManager:
    def __init__(self, agents: List[DebateAgent], topic: str):
        self.agents = agents
        self.topic = topic
        self.conversation_history: List[Dict] = []
        self.current_turn = 0
        self.current_agent_index = 0
        self.current_agent_name: Optional[str] = None
        self.logger = DebateLogger()
        
    async def start_debate(self, debate_prompt: str = None):
        try:
            # Set initial context with more details about the debate
            participants = ", ".join([agent.name for agent in self.agents])
            context = f"""
            Topic: {self.topic}
            Participants: {participants}
            Format: This is a multi-round international debate on AI governance. Each participant will respond in sequence.
            Current Turn: 1 (Opening statement)
            """
            
            # Set current agent to first agent for the first turn
            self.current_agent_name = self.agents[0].name
            
            # Initial message with debate prompt if available
            # For the first message, use an empty last_message since there's no prior message
            first_response = await self.agents[0].generate_response(context, "", debate_prompt)
            self.conversation_history.append({
                "agent": self.agents[0].name,
                "message": first_response,
                "round": 1,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
            self.logger.log_event("Debate Started", f"First response from {self.agents[0].name}")
            return first_response
        except Exception as e:
            self.logger.log_error("Debate Start Error", str(e))
            raise

    async def next_turn(self, debate_prompt: str = None) -> str:
        try:
            # Determine next agent in rotation
            self.current_agent_index = (self.current_agent_index + 1) % len(self.agents)
            current_agent = self.agents[self.current_agent_index]
            
            # Update current agent name
            self.current_agent_name = current_agent.name
            
            # Get last message from the previous speaker
            last_message = self.conversation_history[-1]["message"] if self.conversation_history else ""
            last_speaker = self.conversation_history[-1]["agent"] if self.conversation_history else ""
            
            # Build detailed context including who spoke last
            context = self._build_context()
            
            # Add information about who the agent is responding to
            response_context = f"""
            {context}
            
            You are now responding directly to {last_speaker}'s most recent statement.
            """
            
            # Generate response with debate prompt if available
            response = await current_agent.generate_response(
                context=response_context, 
                last_message=last_message, 
                debate_prompt=debate_prompt
            )
            
            # Add to conversation history with round number
            current_round = self.current_turn + 1
            self.conversation_history.append({
                "agent": current_agent.name,
                "message": response,
                "round": current_round,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
            # Log the debate turn
            self.logger.log_debate_turn(current_agent.name, response)
            
            # Increment turn counter
            self.current_turn += 1
            return response
        except Exception as e:
            self.logger.log_error("Debate Turn Error", str(e))
            raise

    def _build_context(self) -> str:
        """Build context from conversation history"""
        if not self.conversation_history:
            return f"Topic: {self.topic}"
            
        # Include more history for better context (up to 10 messages)
        history_limit = min(10, len(self.conversation_history))
        recent_history = self.conversation_history[-history_limit:]
        
        # Format with round numbers for better tracking
        formatted_history = []
        for msg in recent_history:
            round_num = msg.get("round", "?")
            formatted_history.append(f"Round {round_num} - {msg['agent']}: {msg['message']}")
        
        # Add topic at the beginning
        return f"Topic: {self.topic}\n\n" + "\n\n".join(formatted_history)
                         
    def get_current_agent_name(self) -> str:
        """Get the name of the current agent"""
        return self.current_agent_name or self.agents[0].name