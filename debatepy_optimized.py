import streamlit as st
from debate_manager import DebateManager
from debate_system import DebateAgent
from enhanced_search_integration import TheoreticallyEnhancedAgent, create_enhanced_agents, EnhancedDocumentStore
from perplexity_search import PerplexitySearchClient
from document_retrieval import DocumentStore
import asyncio
import json
import yaml
from datetime import datetime
from debate_logger import DebateLogger
import re
import os
import logging
from typing import Dict, Optional, Any, List
from functools import lru_cache
import time

# PERFORMANCE: Cache configuration loading
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_config_cached():
    """Load and cache configuration with validation"""
    try:
        with open('config.yaml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            
            # Validate required sections
            required_sections = ['agents', 'topics']
            for section in required_sections:
                if section not in config:
                    raise ValueError(f"Configuration missing required '{section}' section")
            
            return config
    except Exception as e:
        st.error(f"Configuration error: {e}")
        st.stop()

# PERFORMANCE: Cache document store initialization
@st.cache_resource
def get_document_store():
    """Initialize and cache document store"""
    try:
        return EnhancedDocumentStore(base_path="agent_documents")
    except Exception as e:
        st.warning(f"Document store initialization failed: {e}")
        return None

# PERFORMANCE: Cache search client initialization  
@st.cache_resource
def get_search_client():
    """Initialize and cache search client"""
    try:
        config = load_config_cached()
        if config.get('search', {}).get('perplexity', {}).get('enabled', False):
            return PerplexitySearchClient(config=config)
        return None
    except Exception as e:
        st.warning(f"Search client initialization failed: {e}")
        return None

# PERFORMANCE: Lightweight debate manager that doesn't recreate heavy objects
class OptimizedDebateManager:
    def __init__(self, selected_topic=None, total_rounds=20, use_documents=True, use_search=True):
        self.config = load_config_cached()
        self.debate_prompt = self.config.get('debate_prompt', '')
        self.total_rounds = total_rounds
        self.conclusion_phase = False
        self.use_documents = use_documents
        self.use_search = use_search
        
        # Use cached resources
        self.document_store = get_document_store() if use_documents else None
        self.search_client = get_search_client() if use_search else None
        
        # Create lightweight agents (cached resources are reused)
        agent_configs = self.config.get('agents', {})
        agent_names = ['openai', 'deepseek', 'european_union']
        self.agents = []
        
        for agent_key in agent_names:
            if agent_key in agent_configs:
                agent_config = agent_configs[agent_key]
                
                agent = TheoreticallyEnhancedAgent(
                    name=agent_config['name'],
                    personality=agent_config['personality'],
                    agent_config_key=agent_key,
                    config=self.config,
                    document_store=self.document_store,
                    search_client=self.search_client
                )
                self.agents.append(agent)
        
        # Set individual agent references
        self.agent_us = self.agents[0]    
        self.agent_china = self.agents[1] 
        self.agent_eu = self.agents[2]    
        self.logger = DebateLogger()
        
        # Handle topic selection
        topics_from_config = self.config.get('topics', [])
        all_topic_names = [t.get('name') for t in topics_from_config if t.get('name')]
        
        topic_info = None
        if selected_topic and selected_topic in all_topic_names:
            topic_info = next((t for t in topics_from_config if t.get('name') == selected_topic), None)
        elif all_topic_names:
            topic_info = topics_from_config[0]  # Use first topic instead of random
        
        if topic_info:
            topic = f"{topic_info.get('name')}: {topic_info.get('description', '')}"
        else:
            raise ValueError("No valid topics found in config.yaml")
        
        self.debate = DebateManager(agents=self.agents, topic=topic)
        
        # Order lists for conclusions and scenarios
        self.conclusion_order = [self.agent_us.name, self.agent_eu.name, self.agent_china.name]
        self.current_conclusion_index = 0
        self.scenario_phase = False
        self.current_scenario_index = 0
        self.scenario_order = [self.agent_us.name, self.agent_eu.name, self.agent_china.name]

    # PERFORMANCE: Simplified response generation with batching option
    async def get_next_response_simple(self, enable_analysis=True) -> Dict[str, Any]:
        """Simplified response generation with optional analysis"""
        try:
            if self.scenario_phase:
                if self.current_scenario_index >= len(self.scenario_order):
                    return {"type": "phase_complete", "phase": "scenarios", "message": "All scenarios presented"}
                
                agent_name_for_scenario = self.scenario_order[self.current_scenario_index]
                current_agent_object = next((agent for agent in self.agents if agent.name == agent_name_for_scenario), None)
                if not current_agent_object:
                    return {"type": "error", "message": f"Agent {agent_name_for_scenario} not found"}
                
                context = self._build_conclusion_context()
                conclusions = getattr(self, '_cached_conclusions', [])
                scenario_message = await current_agent_object.generate_geopolitical_scenario(context, conclusions)
                
                return {
                    "type": "scenario",
                    "agent_name": agent_name_for_scenario,
                    "message": scenario_message,
                    "round": self.current_scenario_index + 1
                }
                
            elif self.conclusion_phase:
                if self.current_conclusion_index >= len(self.conclusion_order):
                    return {"type": "phase_complete", "phase": "conclusions", "message": "All conclusions presented"}
                
                agent_name_to_conclude = self.conclusion_order[self.current_conclusion_index]
                current_agent_object = next((agent for agent in self.agents if agent.name == agent_name_to_conclude), None)
                if not current_agent_object:
                    return {"type": "error", "message": f"Agent {agent_name_to_conclude} not found"}
                
                context = self._build_conclusion_context()
                conclusion_message = await current_agent_object.generate_conclusion(context=context)
                
                return {
                    "type": "conclusion",
                    "agent_name": agent_name_to_conclude,
                    "message": conclusion_message,
                    "round": self.current_conclusion_index + 1
                }
                
            else: # Deliberation phase
                if self.debate.current_turn >= self.total_rounds:
                    return {
                        "type": "transition",
                        "from_phase": "deliberation", 
                        "to_phase": "conclusions",
                        "message": f"After {self.total_rounds} rounds of deliberation on {self.debate.topic}, each representative will now present their final position."
                    }

                round_info_prompt = self.debate_prompt.replace("{round_number}", str(self.debate.current_turn + 1))\
                                                   .replace("{total_rounds}", str(self.total_rounds))
                
                # PERFORMANCE: Use different approach for fast mode
                # Instead of disabling analysis, we'll let the agents generate normally
                # but reduce the complexity of theoretical analysis sections
                
                if not self.debate.conversation_history:
                    response = await self.debate.start_debate(debate_prompt=round_info_prompt)
                else:
                    # Pass fast mode context to agents for lighter analysis
                    if not enable_analysis:
                        # Add fast mode instruction to the prompt
                        fast_mode_prompt = round_info_prompt + "\n\nFAST MODE: Focus on core diplomatic position with minimal theoretical analysis."
                        response = await self.debate.next_turn(debate_prompt=fast_mode_prompt)
                    else:
                        response = await self.debate.next_turn(debate_prompt=round_info_prompt)
                
                return {
                    "type": "deliberation",
                    "agent_name": self.debate.get_current_agent_name(),
                    "message": response,
                    "round": self.debate.current_turn
                }
        except Exception as e:
            return {"type": "error", "message": f"Error generating response: {str(e)}"}
    
    def set_conclusions_cache(self, conclusions: List[Dict[str, Any]]):
        """Set conclusions cache"""
        self._cached_conclusions = conclusions
    
    def _build_conclusion_context(self):
        if not self.debate.conversation_history:
            return f"Topic: {self.debate.topic}"
        return "\n".join([f"{msg['agent']}: {msg['message']}" for msg in self.debate.conversation_history[-10:]])

# PERFORMANCE: Lightweight message formatting
def format_message_simple(message):
    """Simple message formatting without heavy processing"""
    # Basic cleanup only
    if len(message) > 5000:  # Truncate very long messages
        return message[:5000] + "...\n[Message truncated for performance]"
    return message

def main():
    st.set_page_config(
        page_title="AI Futures Deliberation", 
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # PERFORMANCE: Initialize session state efficiently
    session_defaults = {
        'selected_topic': '',
        'num_rounds': 10,
        'debate_initialized': False,
        'conversation': [],
        'turn_count': 0,
        'conclusions': [],
        'current_log_message': "Ready to start",
        'conclusion_phase_active': False,
        'papers_saved': False,
        'scenario_phase_active': False,
        'scenarios': [],
        'image_generation_phase_active': False,
        'generated_images': [],
        'imported_data': None,
        'import_mode': False,
        'fast_mode': False,  # New: Toggle for performance mode
    }
    
    for key, default_value in session_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value
    
    # Load config once
    config = load_config_cached()
    topics_from_config = config.get('topics', [])
    topic_options = [t.get('name') for t in topics_from_config if t.get('name')]
    
    if not topic_options:
        st.error("⚠️ No topics found in config.yaml")
        st.stop()
    
    # Set default topic if not set
    if not st.session_state.selected_topic:
        st.session_state.selected_topic = topic_options[0]

    st.title("🌐 AI Governance Debate")

    # --- PERFORMANCE-OPTIMIZED SIDEBAR ---
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Performance mode toggle
        fast_mode = st.toggle(
            "🚀 Fast Mode",
            value=st.session_state.fast_mode,
            help="Enables faster responses with simplified analysis"
        )
        st.session_state.fast_mode = fast_mode
        
        if fast_mode:
            st.info("⚡ Fast mode enabled - reduced analysis for better performance")
        
        # Topic selection
        st.markdown("**Topic**")
        selected_topic_sb = st.selectbox(
            "Choose topic",
            options=topic_options,
            index=topic_options.index(st.session_state.selected_topic) if st.session_state.selected_topic in topic_options else 0,
            key="sb_topic",
            label_visibility="collapsed"
        )
        
        # Number of rounds
        st.markdown("**Rounds**")
        num_rounds_sb = st.slider(
            "Number of rounds",
            min_value=1,
            max_value=30,
            value=st.session_state.num_rounds,
            key="sb_rounds",
            label_visibility="collapsed"
        )
        
        # Show current configuration compactly
        st.info(f"Current: {st.session_state.num_rounds} rounds")
        
        if st.button("🔄 New Debate", use_container_width=True):
            # Reset state efficiently
            for key in ['debate_initialized', 'conversation', 'turn_count', 'conclusions', 
                       'conclusion_phase_active', 'papers_saved', 'scenario_phase_active', 
                       'scenarios', 'image_generation_phase_active', 'generated_images']:
                st.session_state[key] = session_defaults[key]
            
            st.session_state['selected_topic'] = selected_topic_sb
            st.session_state['num_rounds'] = num_rounds_sb
            st.session_state['current_log_message'] = f"New settings: {num_rounds_sb} rounds on '{selected_topic_sb[:30]}...'"
            
            if 'debate_manager' in st.session_state:
                del st.session_state['debate_manager']
            
            st.rerun()

        # Basic export (simplified)
        if st.session_state.get('debate_initialized', False) and st.session_state.get('turn_count', 0) > 0:
            st.divider()
            if st.button("💾 Export", use_container_width=True):
                export_data = {
                    "topic": st.session_state.debate_manager.debate.topic,
                    "conversation": st.session_state.conversation,
                    "conclusions": st.session_state.conclusions,
                    "export_time": datetime.now().isoformat()
                }
                
                st.download_button(
                    label="📦 Download JSON",
                    data=json.dumps(export_data, indent=2, ensure_ascii=False),
                    file_name=f"debate_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )

    # --- MAIN AREA ---
    if not st.session_state.debate_initialized:
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.info(f"**Topic:** {st.session_state.selected_topic}")
        with col2:
            st.info(f"**Rounds:** {st.session_state.num_rounds}")
        with col3:
            if fast_mode:
                st.success("🚀 Fast Mode")
            else:
                st.info("🔬 Full Analysis")
        
        if st.button("🚀 Start Debate", use_container_width=True):
            with st.spinner("Initializing debate..." + (" (Fast Mode)" if fast_mode else "")):
                start_time = time.time()
                st.session_state.debate_manager = OptimizedDebateManager(
                    st.session_state.selected_topic, 
                    st.session_state.num_rounds
                )
                init_time = time.time() - start_time
                
                st.session_state.debate_initialized = True
                st.session_state.current_log_message = f"Debate initialized in {init_time:.1f}s"
                
            st.rerun()
        
        st.info(st.session_state.current_log_message)
        return

    # Debate interface for initialized debate
    debate_manager = st.session_state.debate_manager
    topic = debate_manager.debate.topic
    
    st.markdown(f"### {topic}")
    
    # Agent info
    participants = f"🇺🇸 **{debate_manager.agent_us.name}** | 🇨🇳 **{debate_manager.agent_china.name}** | 🇪🇺 **{debate_manager.agent_eu.name}**"
    st.markdown(participants)
    
    # Status message
    st.info(st.session_state.current_log_message)

    # --- SIMPLIFIED CONTROL PANEL ---
    st.markdown("### Control Panel")
    
    current_phase = ""
    if st.session_state.image_generation_phase_active:
        current_phase = "Phase 4: Posters"
    elif st.session_state.scenario_phase_active:
        current_phase = f"Phase 3: Scenarios ({len(st.session_state.scenarios)}/3)"
    elif st.session_state.conclusion_phase_active:
        current_phase = f"Phase 2: Papers ({len(st.session_state.conclusions)}/3)"
    else:
        progress = min(st.session_state.turn_count / st.session_state.num_rounds, 1.0)
        st.progress(progress)
        current_phase = f"Phase 1: Debate - Round {st.session_state.turn_count}/{st.session_state.num_rounds}"
    
    st.caption(current_phase)

    # PERFORMANCE: Single button logic with fast mode
    if not st.session_state.conclusion_phase_active and st.session_state.turn_count < st.session_state.num_rounds:
        button_text = f"▶️ Round {debate_manager.debate.current_turn + 1}"
        if fast_mode:
            button_text += " (Fast)"
        
        if st.button(button_text, use_container_width=True):
            with st.spinner(f"Generating Round {debate_manager.debate.current_turn + 1}..."):
                start_time = time.time()
                
                # Use simplified response generation in fast mode
                response_data = asyncio.run(
                    debate_manager.get_next_response_simple(enable_analysis=not fast_mode)
                )
                
                response_time = time.time() - start_time
                
                if response_data.get("type") == "deliberation":
                    st.session_state.conversation.append({
                        "agent": response_data["agent_name"],
                        "message": format_message_simple(response_data["message"]),
                        "round": response_data["round"],
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    st.session_state.turn_count = response_data["round"]
                    st.session_state.current_log_message = f"Round {st.session_state.turn_count} completed in {response_time:.1f}s"
                elif response_data.get("type") == "transition":
                    st.session_state.conclusion_phase_active = True
                    debate_manager.conclusion_phase = True
                    debate_manager.current_conclusion_index = 0
                    st.session_state.current_log_message = response_data["message"]
                else:
                    st.session_state.current_log_message = f"Error: {response_data.get('message', 'Unknown error')}"
            
            st.rerun()

    # Continue with other phases (simplified)...
    elif st.session_state.turn_count >= st.session_state.num_rounds and not st.session_state.conclusion_phase_active:
        if st.button("📜 Generate Position Papers", use_container_width=True):
            st.session_state.conclusion_phase_active = True
            debate_manager.conclusion_phase = True
            st.rerun()
    
    # Show simplified conversation view
    if st.session_state.conversation:
        st.markdown("### Debate Transcript")
        
        # PERFORMANCE: Show only recent messages by default
        max_display = 10 if fast_mode else len(st.session_state.conversation)
        recent_messages = st.session_state.conversation[-max_display:]
        
        if len(st.session_state.conversation) > max_display:
            st.caption(f"Showing {max_display} most recent of {len(st.session_state.conversation)} total messages")
        
        for message_data in recent_messages:
            agent_name = message_data["agent"]
            avatar = "🇺🇸" 
            if "China" in agent_name: avatar = "🇨🇳"
            elif "European" in agent_name: avatar = "🇪🇺"
            
            with st.chat_message(agent_name, avatar=avatar):
                st.markdown(f"**{agent_name} (Round {message_data.get('round', '?')})**")
                
                # PERFORMANCE: Simplified message display in fast mode
                message_content = message_data["message"]
                if fast_mode and len(message_content) > 2000:
                    # Show summary in fast mode
                    st.markdown(message_content[:2000] + "\n\n*[Truncated in fast mode]*")
                    with st.expander("Show full message"):
                        st.markdown(message_content)
                else:
                    st.markdown(message_content)

    # Show performance stats in debug mode
    if st.checkbox("Show performance stats"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Messages", len(st.session_state.conversation))
        with col2:
            st.metric("Mode", "Fast" if fast_mode else "Full")
        with col3:
            cache_info = load_config_cached.cache_info() if hasattr(load_config_cached, 'cache_info') else None
            if cache_info:
                st.metric("Config Cache Hits", cache_info.hits)

if __name__ == "__main__":
    main()
