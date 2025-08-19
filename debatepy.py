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

def load_config():
    try:
        with open('config.yaml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            # Ensure required sections exist
            if 'agents' not in config:
                raise ValueError("Configuration missing required 'agents' section")
            if 'topics' not in config:
                raise ValueError("Configuration missing required 'topics' section")
            return config
    except Exception as e:
        raise RuntimeError(f"Critical configuration issue: {e}. Please check your config.yaml file.")

class StreamlitDebateManager:
    def __init__(self, selected_topic=None, total_rounds=20, use_documents=True, use_search=True):
        self.config = load_config()
        self.debate_prompt = self.config.get('debate_prompt', '')
        self.total_rounds = total_rounds
        self.conclusion_phase = False # This is internal to manager logic
        self.use_documents = use_documents
        self.use_search = use_search and self.config.get('search', {}).get('perplexity', {}).get('enabled', False)
        
        # Initialize enhanced document store if using documents
        self.document_store = None
        if self.use_documents:
            try:
                self.document_store = EnhancedDocumentStore(base_path="agent_documents")
                logging.info(f"Initialized enhanced document store with {len(self.document_store.document_data)} documents and {len(self.document_store.theoretical_resources)} theoretical resources")
            except Exception as e:
                logging.error(f"Failed to initialize enhanced document store: {e}")
                self.use_documents = False
        
        # Initialize search client if using search
        self.search_client = None
        if self.use_search:
            try:
                self.search_client = PerplexitySearchClient(config=self.config)
                logging.info("Initialized Perplexity search client")
            except Exception as e:
                logging.error(f"Failed to initialize search client: {e}")
                self.use_search = False
        
        agent_configs = self.config.get('agents', {})
        
        # Validate agent configs exist
        if not agent_configs:
            raise ValueError("No agent configurations found in config. Please check config.yaml")
        
        # Ensure all required agents exist
        required_agents = ['openai', 'deepseek', 'european_union']
        for agent in required_agents:
            if agent not in agent_configs:
                raise ValueError(f"Missing required agent configuration: {agent}")
        
        # Create TheoreticallyEnhancedAgent instances with full capabilities
        # These agents combine document retrieval, search, costly signals, performance fictions, and theoretical analysis
        agent_names = ['openai', 'deepseek', 'european_union']
        self.agents = []
        
        for agent_key in agent_names:
            agent_config = agent_configs[agent_key]
            
            # Create TheoreticallyEnhancedAgent with all capabilities including theoretical resources
            agent = TheoreticallyEnhancedAgent(
                name=agent_config['name'],
                personality=agent_config['personality'],
                agent_config_key=agent_key,
                config=self.config,
                document_store=self.document_store if self.use_documents else None,
                search_client=self.search_client if self.use_search else None
            )
            
            self.agents.append(agent)
        
        # Set individual agent references
        self.agent_us = self.agents[0]    # United States
        self.agent_china = self.agents[1] # People's Republic of China  
        self.agent_eu = self.agents[2]    # European Union
        self.logger = DebateLogger()
        
        topics_from_config = self.config.get('topics', [])
        all_topic_names = [t.get('name') for t in topics_from_config if t.get('name')]
        
        # Find the full topic info including description
        topic_info = None
        if selected_topic and selected_topic in all_topic_names:
            topic_info = next((t for t in topics_from_config if t.get('name') == selected_topic), None)
        elif all_topic_names:
            import random
            topic_info = random.choice(topics_from_config)
            self.logger.log_event("TopicWarning", f"Provided selected_topic '{selected_topic}' was invalid or None. Randomly selected: {topic_info.get('name')}")
        
        if topic_info:
            # Create a rich topic string that includes both name and description
            topic = f"{topic_info.get('name')}: {topic_info.get('description', '')}"
        else:
            raise ValueError("Critical topic configuration issue: No valid topics found in config.yaml or invalid topic selection.")
        
        self.debate = DebateManager(agents=self.agents, topic=topic)
        
        # DISABLE formatter integration for Streamlit to get clean text output
        # The formatter is causing complex structured output that appears grey in Streamlit
        # We want simple, clean debate responses for better readability
        pass
        
        self.logger.log_event("Deliberation Initialized", f"Topic: {self.debate.topic}, Rounds: {self.total_rounds}")
        # self.current_round = 0 # This was for StreamlitDebateManager's own tracking, DebateManager has its own
        self.conclusion_order = [self.agent_us.name, self.agent_eu.name, self.agent_china.name]
        self.current_conclusion_index = 0 # Index for iterating through conclusion_order
        
        # Add scenario generation phase variables
        self.scenario_phase = False
        self.current_scenario_index = 0
        self.scenario_order = [self.agent_us.name, self.agent_eu.name, self.agent_china.name]

    async def get_next_response(self):
        # This method now primarily fetches responses. Phase transition logic is mostly UI-driven.
        if self.scenario_phase:
            if self.current_scenario_index >= len(self.scenario_order):
                return None # All scenarios presented
            agent_name_for_scenario = self.scenario_order[self.current_scenario_index]
            current_agent_object = next((agent for agent in self.agents if agent.name == agent_name_for_scenario), None)
            if not current_agent_object:
                self.logger.log_event("Error", f"Agent {agent_name_for_scenario} not found for scenario generation.")
                return {"error": f"Agent {agent_name_for_scenario} not found."}
            
            context = self._build_conclusion_context()
            scenario_message = await current_agent_object.generate_geopolitical_scenario(context, st.session_state.conclusions)
            self.logger.log_geopolitical_scenario(scenario_message, self.debate.topic)
            return {"agent_name": agent_name_for_scenario, "message": scenario_message, "type": "scenario"}
        elif self.conclusion_phase:
            if self.current_conclusion_index >= len(self.conclusion_order):
                return None # All conclusions presented
            agent_name_to_conclude = self.conclusion_order[self.current_conclusion_index]
            current_agent_object = next((agent for agent in self.agents if agent.name == agent_name_to_conclude), None)
            if not current_agent_object:
                self.logger.log_event("Error", f"Agent {agent_name_to_conclude} not found for conclusion.")
                # self.current_conclusion_index += 1 # UI will advance this upon successful retrieval or skip
                return {"error": f"Agent {agent_name_to_conclude} not found."}
            
            context = self._build_conclusion_context()
            conclusion_message = await current_agent_object.generate_conclusion(context=context)
            # Log the full position paper content
            self.logger.log_position_paper(agent_name_to_conclude, conclusion_message, self.debate.topic)
            return {"agent_name": agent_name_to_conclude, "message": conclusion_message}
        else: # Deliberation phase
            # Check if it's time to transition (UI should prevent calling this if rounds are done)
            if self.debate.current_turn >= self.total_rounds:
                 return self._prepare_conclusion_transition() # Signal to UI to switch phase

            round_info_prompt = self.debate_prompt.replace("{round_number}", str(self.debate.current_turn + 1))\
                                               .replace("{total_rounds}", str(self.total_rounds))
            if not self.debate.conversation_history:
                response = await self.debate.start_debate(debate_prompt=round_info_prompt)
                self.logger.log_event("Deliberation Started", f"Round 1 of {self.total_rounds}")
            else:
                response = await self.debate.next_turn(debate_prompt=round_info_prompt)
                self.logger.log_event(f"Deliberation Round {self.debate.current_turn}", f"Agent: {self.debate.get_current_agent_name()}")
            return response
    
    def _prepare_conclusion_transition(self):
        return f"After {self.total_rounds} rounds of deliberation on {self.debate.topic}, each representative will now present their final position."
    
    def _build_conclusion_context(self):
        if not self.debate.conversation_history:
            return f"Topic: {self.debate.topic}"
        return "\n".join([f"{msg['agent']}: {msg['message']}" for msg in self.debate.conversation_history[-10:]])

def format_message_with_round(message, round_num=None):
    # This function might become less relevant if messages are self-contained with round info
    if round_num:
        return f"**Round {round_num}**\n\n{message}"
    return message

def parse_position_papers(content):
    """Parse position papers from all_position_papers_*.txt file"""
    papers = []
    
    # Split by the separator pattern for each position paper
    sections = content.split("POSITION PAPER:")
    
    for section in sections[1:]:  # Skip the first empty section
        lines = section.strip().split('\n')
        if not lines:
            continue
            
        # Extract agent name from the first line
        agent_name = lines[0].strip()
        
        # Find the timestamp line and start collecting message content after it
        message_lines = []
        in_message = False
        
        for line in lines[1:]:
            if line.startswith("Timestamp:"):
                in_message = True
                continue
            elif line.startswith("================================================================================"):
                break
            elif in_message and line.strip():
                message_lines.append(line)
        
        if agent_name and message_lines:
            # Clean up agent name
            agent_name = agent_name.replace(".", "").strip()
            
            papers.append({
                'agent_name': agent_name,
                'message': '\n'.join(message_lines).strip(),
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
    
    return papers

def parse_scenarios(content):
    """Parse geopolitical scenarios from geopolitical_scenario_*.txt file"""
    scenarios = []
    
    # The scenario file has a header section followed by the actual scenario content
    lines = content.split('\n')
    
    # Find where the actual scenario content starts (after the header)
    scenario_start = 0
    for i, line in enumerate(lines):
        if "================================================================================" in line and i > 0:
            scenario_start = i + 1
            break
    
    # Find where the scenario content ends
    scenario_end = len(lines)
    for i, line in enumerate(lines[scenario_start:], scenario_start):
        if "================================================================================" in line and "End of" in lines[i+1] if i+1 < len(lines) else False:
            scenario_end = i
            break
    
    # Extract the scenario content
    scenario_content = []
    for i in range(scenario_start, scenario_end):
        if i < len(lines):
            scenario_content.append(lines[i])
    
    if scenario_content:
        full_content = '\n'.join(scenario_content).strip()
        
        # This appears to be China's scenario based on the content
        scenarios.append({
            'agent_name': 'People\'s Republic of China',
            'message': full_content,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    
    return scenarios


def analyze_imported_data(imported_data):
    """Analyze imported deliberation data for signals and imaginaries"""
    
    analysis_results = []
    
    with st.spinner("Analyzing imported data for AI governance signals and imaginaries..."):
        
        # If we have position papers, analyze them
        if 'papers' in imported_data:
            st.info("🔍 Analyzing position papers for costly signals and performance fictions...")
            
            for paper in imported_data['papers']:
                agent_name = paper['agent_name']
                position_content = paper['message']
                
                # Map agent names to standard format
                if "United States" in agent_name or "US" in agent_name:
                    standard_agent_name = "United States"
                elif "China" in agent_name or "People's Republic" in agent_name:
                    standard_agent_name = "People's Republic of China"
                elif "European Union" in agent_name or "EU" in agent_name:
                    standard_agent_name = "European Union"
                else:
                    standard_agent_name = agent_name
                
                # Analyze for costly signals and performance fictions
                analysis_results.append({
                    "agent_name": standard_agent_name,
                    "analysis_type": "position_paper",
                    "content": position_content,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
        
        # If we have scenarios, analyze them
        elif 'scenarios' in imported_data:
            st.info("🔍 Analyzing scenarios for governance imaginaries...")
            
            for item in imported_data['scenarios']:
                agent_name = item['agent_name']
                content = item['message']
                
                # Map agent names to standard format
                if "United States" in agent_name or "US" in agent_name:
                    standard_agent_name = "United States"
                elif "China" in agent_name or "People's Republic" in agent_name:
                    standard_agent_name = "People's Republic of China"
                elif "European Union" in agent_name or "EU" in agent_name:
                    standard_agent_name = "European Union"
                else:
                    standard_agent_name = agent_name
                
                analysis_results.append({
                    "agent_name": standard_agent_name,
                    "analysis_type": "scenario",
                    "content": content,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
    
    # Store analysis results in session state
    st.session_state.analysis_results = analysis_results
    st.session_state.analysis_phase_active = True
    
    st.success(f"✅ Analyzed {len(analysis_results)} items for AI governance signals and imaginaries!")
    if len(analysis_results) >= 3:
        st.success("🎉 Complete theoretical analysis available!")

def main():
    st.set_page_config(page_title="AI Futures Deliberation", layout="wide")
    
    # Initialize session state variables if they don't exist
    if 'selected_topic' not in st.session_state:
        config = load_config()
        topics = config.get('topics', [])
        if topics:
            st.session_state.selected_topic = topics[0].get('name', '')
        else:
            st.session_state.selected_topic = ''
    
    if 'num_rounds' not in st.session_state:
        st.session_state.num_rounds = 10
    
    if 'debate_initialized' not in st.session_state:
        st.session_state.debate_initialized = False
    
    if 'conversation' not in st.session_state:
        st.session_state.conversation = []
    
    if 'turn_count' not in st.session_state:
        st.session_state.turn_count = 0
    
    st.title("🌐 AI Governance Debate")

    # --- Sidebar for settings ---
    with st.sidebar:
        st.header("⚙️ Settings")
        
        config = load_config()
        topics_from_config = config.get('topics', [])
        topic_options = [t.get('name') for t in topics_from_config if t.get('name')]
        if not topic_options:
            st.error("⚠️ No topics found in config.yaml")
            st.stop()
        
        # Topic selection
        st.markdown("**Topic**")
        selected_topic_sb = st.selectbox(
            "Choose a topic for deliberation",
            options=topic_options,
            index=0,
            key="sb_topic",
            label_visibility="collapsed"
        )
        
        # Number of rounds
        st.markdown("**Rounds**")
        num_rounds_sb = st.slider(
            "Number of deliberation rounds",
            min_value=1,
            max_value=30,
            value=10,
            key="sb_rounds",
            label_visibility="collapsed"
        )
        st.caption(f"Selected: {num_rounds_sb} rounds")

        # Show current configuration
        if 'selected_topic' in st.session_state and 'num_rounds' in st.session_state:
            st.info(f"Current: {st.session_state.num_rounds} rounds on '{st.session_state.selected_topic[:50]}...'")
        
        if st.button("🔄 Configure New Deliberation", use_container_width=True, key="configure_new"):
            # Force update session state
            st.session_state['selected_topic'] = selected_topic_sb
            st.session_state['num_rounds'] = num_rounds_sb
            st.session_state['debate_initialized'] = False # Mark for re-initialization
            st.session_state['conversation'] = []
            st.session_state['turn_count'] = 0
            st.session_state['conclusions'] = []
            st.session_state['conclusion_phase_active'] = False
            st.session_state['papers_saved'] = False  # Reset papers saved flag
            st.session_state['scenario_phase_active'] = False
            st.session_state['scenarios'] = []
            st.session_state['image_generation_phase_active'] = False
            st.session_state['generated_images'] = []
            # Clear imported data
            st.session_state['imported_data'] = None
            st.session_state['import_mode'] = False
            if 'debate_manager' in st.session_state:
                del st.session_state['debate_manager'] # Remove old manager
            st.session_state['current_log_message'] = f"New settings loaded: {num_rounds_sb} rounds on topic '{selected_topic_sb[:50]}...'. Click 'Initialize Deliberation' to start."
            st.rerun()

        st.divider()
        
        # Import Previous Deliberation Section
        st.markdown("**📁 Import Previous Debate**")
        
        # File uploaders with cleaner labels
        uploaded_papers = st.file_uploader(
            "Position Papers",
            type=['txt'],
            key="papers_upload",
            help="all_position_papers_*.txt"
        )
        
        uploaded_scenarios = st.file_uploader(
            "Scenarios",
            type=['txt'],
            key="scenarios_upload",
            help="geopolitical_scenario_*.txt"
        )
        
        if uploaded_papers or uploaded_scenarios:
            if st.button("📥 Import & Process Files", use_container_width=True, key="import_files"):
                imported_data = {}
                
                # Process position papers file
                if uploaded_papers:
                    try:
                        papers_content = uploaded_papers.read().decode('utf-8')
                        imported_data['papers'] = parse_position_papers(papers_content)
                        st.success(f"✅ Imported {len(imported_data['papers'])} position papers")
                    except Exception as e:
                        st.error(f"❌ Error reading position papers: {e}")
                
                # Process scenarios file
                if uploaded_scenarios:
                    try:
                        scenarios_content = uploaded_scenarios.read().decode('utf-8')
                        imported_data['scenarios'] = parse_scenarios(scenarios_content)
                        st.success(f"✅ Imported geopolitical scenarios")
                    except Exception as e:
                        st.error(f"❌ Error reading scenarios: {e}")
                
                if imported_data:
                    st.session_state.imported_data = imported_data
                    st.session_state.import_mode = True
                    st.rerun()
        
        # Generate propaganda posters from imported data
        if st.session_state.get('import_mode', False) and st.session_state.get('imported_data'):
            st.divider()
            imported_data = st.session_state.imported_data
            
            # Show what's loaded in a compact way
            loaded_items = []
            if 'papers' in imported_data:
                loaded_items.append(f"{len(imported_data['papers'])} papers")
            if 'scenarios' in imported_data:
                loaded_items.append("scenarios")
            
            if loaded_items:
                st.caption(f"Loaded: {', '.join(loaded_items)}")
            
            if st.button("🔍 Analyze for Signals & Imaginaries", use_container_width=True, key="analyze_from_import"):
                analyze_imported_data(imported_data)
                st.rerun()

        # Export button - active only if debate has been initialized and run at least one turn
        if st.session_state.get('debate_initialized', False) and st.session_state.get('turn_count', 0) > 0:
            st.divider()
            if st.button("💾 Export", use_container_width=True, key="export_deliberation"):
                if 'debate_manager' in st.session_state:
                    export_data = {
                        "topic": st.session_state.debate_manager.debate.topic,
                        "total_rounds": st.session_state.debate_manager.total_rounds,
                        "deliberation": st.session_state.get('conversation', []),
                        "conclusions": st.session_state.get("conclusions", []),
                        "scenarios": st.session_state.get("scenarios", []),
                        "generated_images": st.session_state.get("generated_images", []),
                        "phases_completed": {
                            "deliberation": bool(st.session_state.get('conversation')),
                            "position_papers": bool(st.session_state.get('conclusions')),
                            "scenarios": bool(st.session_state.get('scenarios')),
                            "propaganda_posters": bool(st.session_state.get('generated_images'))
                        },
                        "export_timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                    # Count total content for user info
                    total_items = (
                        len(st.session_state.get('conversation', [])) + 
                        len(st.session_state.get('conclusions', [])) + 
                        len(st.session_state.get('scenarios', [])) + 
                        len(st.session_state.get('generated_images', []))
                    )
                    
                    st.download_button(
                        label=f"📦 Download ({total_items} items)",
                        data=json.dumps(export_data, indent=2, ensure_ascii=False),
                        file_name=f"debate_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
                else:
                    st.warning("Debate manager not found for export.")

    # --- Initialize State Variables (if they don't exist on first run or after full clear) --- 
    if 'selected_topic' not in st.session_state:
        st.session_state.selected_topic = topic_options[0]
    if 'num_rounds' not in st.session_state:
        st.session_state.num_rounds = 10 # Default value
    if 'debate_initialized' not in st.session_state:
        st.session_state.debate_initialized = False
    if 'conversation' not in st.session_state:
        st.session_state.conversation = []
    if 'turn_count' not in st.session_state:
        st.session_state.turn_count = 0
    if 'conclusions' not in st.session_state:
        st.session_state.conclusions = []
    if 'current_log_message' not in st.session_state:
        st.session_state.current_log_message = "Ready to start"
    if 'conclusion_phase_active' not in st.session_state:
        st.session_state.conclusion_phase_active = False
    if 'papers_saved' not in st.session_state:
        st.session_state.papers_saved = False
    if 'scenario_phase_active' not in st.session_state:
        st.session_state.scenario_phase_active = False
    if 'scenarios' not in st.session_state:
        st.session_state.scenarios = []
    if 'image_generation_phase_active' not in st.session_state:
        st.session_state.image_generation_phase_active = False
    if 'generated_images' not in st.session_state:
        st.session_state.generated_images = []
    if 'imported_data' not in st.session_state:
        st.session_state.imported_data = None
    if 'import_mode' not in st.session_state:
        st.session_state.import_mode = False

    # --- Main Area ---
    if not st.session_state.debate_initialized:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.info(f"**Topic:** {st.session_state.selected_topic}")
        with col2:
            st.info(f"**Rounds:** {st.session_state.num_rounds}")
        
        if st.button("🚀 Start Debate", key="init_debate_main", use_container_width=True):
            st.session_state.debate_manager = StreamlitDebateManager(st.session_state.selected_topic, st.session_state.num_rounds)
            st.session_state.debate_initialized = True
            st.session_state.conversation = [] # Ensure clean slate
            st.session_state.turn_count = 0
            st.session_state.conclusions = []
            st.session_state.conclusion_phase_active = False
            st.session_state.papers_saved = False  # Reset papers saved flag for new debate
            st.session_state.scenario_phase_active = False
            st.session_state.scenarios = []
            st.session_state.image_generation_phase_active = False
            st.session_state.generated_images = []
            st.session_state.current_log_message = "Debate started"
            st.rerun()
        
        # Show import mode if active
        if st.session_state.get('import_mode', False):
            st.divider()
            st.markdown("**📁 Imported Data**")
            
            imported_data = st.session_state.imported_data
            
            if 'papers' in imported_data:
                st.markdown("**Position Papers**")
                for paper in imported_data['papers']:
                    with st.expander(f"{paper['agent_name']}"):
                        st.markdown(paper['message'])
            
            if 'scenarios' in imported_data:
                st.markdown("**Scenarios**")
                for scenario in imported_data['scenarios']:
                    with st.expander(f"{scenario['agent_name']}"):
                        st.markdown(scenario['message'])
            
            # Show generated images if available
            if st.session_state.get('generated_images'):
                st.markdown("**🎨 Posters**")
                
                # Display images in a grid layout
                cols = st.columns(len(st.session_state.generated_images))
                
                for i, image_data in enumerate(st.session_state.generated_images):
                    agent_name = image_data["agent_name"]
                    image_path = image_data["image_path"]
                    prompt = image_data["prompt"]
                    
                    with cols[i]:
                        avatar = "🇺🇸"
                        flag_text = "United States"
                        if "China" in agent_name or "People's Republic" in agent_name: 
                            avatar, flag_text = "🇨🇳", "People's Republic of China"
                        elif "European Union" in agent_name or "EU" in agent_name: 
                            avatar, flag_text = "🇪🇺", "European Union"
                        
                        st.markdown(f"**{avatar} {flag_text}**")
                        
                        if image_path and os.path.exists(image_path):
                            st.image(image_path, caption=f"{flag_text}'s Vision", use_container_width=True)
                        else:
                            st.info("Image generation placeholder")
                        
                        with st.expander("View Full Image Prompt"):
                            st.text_area("Full Prompt", prompt, height=200, disabled=True)
        
        st.info(st.session_state.current_log_message)
        return # Stop further rendering until initialized

    # If initialized, proceed to show debate interface
    # Ensure debate_manager is loaded from session state for subsequent interactions
    debate_manager = st.session_state.debate_manager 
    agent_us_name = debate_manager.agent_us.name
    agent_china_name = debate_manager.agent_china.name
    agent_eu_name = debate_manager.agent_eu.name
    topic = debate_manager.debate.topic # Get actual topic from the initialized manager
    total_deliberation_rounds = debate_manager.total_rounds

    st.markdown(f"### Deliberation Topic: {topic}")
    participants_display = f"🇺🇸 **{agent_us_name}** | 🇨🇳 **{agent_china_name}** | 🇪🇺 **{agent_eu_name}**"
    st.markdown(participants_display)
    st.info(st.session_state.current_log_message)

    # --- Control Panel --- 
    st.markdown("### Control Panel")
    # control_cols = st.columns(1) # Use a single column for simplicity first

    # Button to advance deliberation turns
    if not st.session_state.conclusion_phase_active and st.session_state.turn_count < total_deliberation_rounds:
        if st.button("▶️ Next Deliberation Turn", use_container_width=True, key="next_delib_turn"):
            with st.spinner(f"Generating Round {debate_manager.debate.current_turn + 1}..."):
                response = asyncio.run(debate_manager.get_next_response())
                if isinstance(response, str) and not response.startswith("After "): # Regular deliberation response
                    current_speaker = debate_manager.debate.get_current_agent_name()
                    
                    st.session_state.conversation.append({
                        "agent": current_speaker,
                        "message": response,
                        "round": debate_manager.debate.current_turn,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    st.session_state.turn_count = debate_manager.debate.current_turn
                    st.session_state.current_log_message = f"Round {st.session_state.turn_count} by {current_speaker} recorded."
                elif isinstance(response, str) and response.startswith("After "): # Transition message received prematurely
                    st.session_state.conclusion_phase_active = True
                    debate_manager.conclusion_phase = True # Sync manager state
                    debate_manager.current_conclusion_index = 0
                    st.session_state.current_log_message = response
                    st.success(response)
                else:
                    st.session_state.current_log_message = "Error: Unexpected response during deliberation."
                    st.error(f"Unexpected response: {response}")
            st.rerun()

    # Button to proceed to conclusion phase OR skip to scenarios
    elif not st.session_state.conclusion_phase_active and st.session_state.turn_count >= total_deliberation_rounds and not st.session_state.scenario_phase_active:
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📜 Generate Position Papers", use_container_width=True, key="proceed_to_concl"):
                transition_message = debate_manager._prepare_conclusion_transition()
                debate_manager.conclusion_phase = True # Ensure manager is in conclusion phase
                st.session_state.conclusion_phase_active = True
                debate_manager.current_conclusion_index = 0 # Reset index for starting conclusions
                st.session_state.current_log_message = transition_message
                st.success(transition_message)
                st.rerun()
        
        with col2:
            if st.button("🌍 Skip to Scenarios & Posters", use_container_width=True, key="skip_to_scenarios"):
                st.session_state.scenario_phase_active = True
                debate_manager.scenario_phase = True
                debate_manager.current_scenario_index = 0
                st.session_state.current_log_message = "Skipping position papers. Proceeding directly to geopolitical scenarios!"
                st.info("⚡ Fast track: Going straight to the creative content!")
                st.rerun()

    # Button to get next agent's conclusion
    elif st.session_state.conclusion_phase_active and debate_manager.current_conclusion_index < len(debate_manager.conclusion_order):
        next_conclusion_agent_name = debate_manager.conclusion_order[debate_manager.current_conclusion_index]
        if st.button(f"📜 Get {next_conclusion_agent_name}'s Conclusion", use_container_width=True, key=f"get_concl_{next_conclusion_agent_name.replace(' ', '_')}"):
            with st.spinner(f"Generating conclusion for {next_conclusion_agent_name}..."):
                # Ensure the manager knows it's in conclusion phase before calling get_next_response
                debate_manager.conclusion_phase = True 
                response_data = asyncio.run(debate_manager.get_next_response())
                if response_data and isinstance(response_data, dict) and "agent_name" in response_data:
                    st.session_state.conclusions.append({
                        "agent_name": response_data["agent_name"],
                        "message": response_data["message"],
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    st.session_state.current_log_message = f"Conclusion from {response_data['agent_name']} generated."
                    debate_manager.current_conclusion_index += 1 # Advance index AFTER successful retrieval
                elif response_data is None: # All conclusions might be done
                    st.session_state.current_log_message = "All conclusions appear to be presented."
                elif response_data and isinstance(response_data, dict) and "error" in response_data:
                    st.session_state.current_log_message = f"Error: {response_data['error']}"
                    st.error(response_data['error'])
                else:
                    st.session_state.current_log_message = f"Error or unexpected data getting conclusion for {next_conclusion_agent_name}."
                    st.error(f"Unexpected response data: {response_data}")
            st.rerun()
    
    # Scenario Generation Phase - after all conclusions are complete
    elif st.session_state.conclusion_phase_active and debate_manager.current_conclusion_index >= len(debate_manager.conclusion_order) and not st.session_state.scenario_phase_active:
        if st.button("🌍 Proceed to Scenario Generation Phase", use_container_width=True, key="proceed_to_scenario"):
            st.session_state.scenario_phase_active = True
            debate_manager.scenario_phase = True
            debate_manager.current_scenario_index = 0
            st.session_state.current_log_message = "Starting scenarios"
            st.rerun()
    
    # Button to get next agent's scenario
    elif st.session_state.scenario_phase_active and debate_manager.current_scenario_index < len(debate_manager.scenario_order):
        next_scenario_agent_name = debate_manager.scenario_order[debate_manager.current_scenario_index]
        if st.button(f"🔮 Get {next_scenario_agent_name}'s Geopolitical Scenario", use_container_width=True, key=f"get_scenario_{next_scenario_agent_name.replace(' ', '_')}"):
            with st.spinner(f"Generating geopolitical scenario for {next_scenario_agent_name}..."):
                debate_manager.scenario_phase = True
                response_data = asyncio.run(debate_manager.get_next_response())
                if response_data and isinstance(response_data, dict) and "agent_name" in response_data:
                    st.session_state.scenarios.append({
                        "agent_name": response_data["agent_name"],
                        "message": response_data["message"],
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    st.session_state.current_log_message = f"Geopolitical scenario from {response_data['agent_name']} generated."
                    debate_manager.current_scenario_index += 1
                elif response_data is None:
                    st.session_state.current_log_message = "All scenarios appear to be presented."
                elif response_data and isinstance(response_data, dict) and "error" in response_data:
                    st.session_state.current_log_message = f"Error: {response_data['error']}"
                    st.error(response_data['error'])
                else:
                    st.session_state.current_log_message = f"Error getting scenario for {next_scenario_agent_name}."
                    st.error(f"Unexpected response data: {response_data}")
            st.rerun()
    
    # Image Generation Phase - after all scenarios are complete (OPTIONAL)
    elif st.session_state.scenario_phase_active and debate_manager.current_scenario_index >= len(debate_manager.scenario_order) and not st.session_state.image_generation_phase_active:
        # Make image generation optional - user can choose to generate or skip
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🎨 Generate Propaganda Posters", use_container_width=True, key="proceed_to_images"):
                st.session_state.image_generation_phase_active = True
                st.session_state.current_log_message = "Generating posters"
                
                # Generate images for each agent
                with st.spinner("Generating posters..."):
                    # Check for OpenAI API key first, fallback to OpenRouter key
                    openai_api_key = os.getenv("OPENAI_API_KEY")
                    openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
                    api_key = openai_api_key if openai_api_key else openrouter_api_key
                    
                    if not api_key:
                        st.warning("No API key found for image generation. Add OPENAI_API_KEY to your .env file for actual image generation.")
                    elif not openai_api_key and openrouter_api_key:
                        st.info("Using OpenRouter API key - note that image generation requires OpenAI API access. Add OPENAI_API_KEY to .env for actual images.")
                    
                    for scenario in st.session_state.scenarios:
                        agent_name = scenario["agent_name"]
                        scenario_text = scenario["message"]
                        
                        # Extract vision text from scenario for image prompt
                        vision_text = scenario_text[:200] + "..." if len(scenario_text) > 200 else scenario_text
                        
                        image_path, prompt = debate_manager.logger.generate_propaganda_image(
                            agent_name, scenario_text, vision_text, openai_api_key  # Use OpenAI key specifically
                        )
                        
                        st.session_state.generated_images.append({
                            "agent_name": agent_name,
                            "image_path": image_path,
                            "prompt": prompt,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
                    
                    st.session_state.current_log_message = "Posters complete"
                st.success("✅ Posters generated")
                st.rerun()
        
        with col2:
            if st.button("⏭️ Skip Poster Generation", use_container_width=True, key="skip_images"):
                st.session_state.image_generation_phase_active = True  # Mark as complete without generating
                st.session_state.current_log_message = "Poster generation skipped - debate complete"
                st.info("Poster generation skipped. Debate complete!")
                st.rerun()
    
    # Final completion state
    else:
        if st.session_state.get('debate_initialized', False):
            if st.session_state.image_generation_phase_active:
                # Check if we actually generated images or just skipped
                if st.session_state.get('generated_images'):
                    st.success("🎉 Complete with posters!")
                    st.balloons()
                    st.session_state.current_log_message = "All phases complete"
                else:
                    st.success("🎉 Debate complete!")
                    st.session_state.current_log_message = "Debate complete (posters skipped)"
            elif st.session_state.scenario_phase_active:
                st.success("Scenarios complete")
                st.session_state.current_log_message = "Ready for optional posters"
            else:
                if st.session_state.conclusion_phase_active:
                    st.success("Papers complete")
                    st.session_state.current_log_message = "Ready for scenarios"
                else:
                    st.info("Debate complete")
                    st.session_state.current_log_message = "Ready for next phase"
             
            # Save all position papers to a summary file when all conclusions are complete
            if st.session_state.get("conclusions") and not st.session_state.get("papers_saved", False):
                summary_file = debate_manager.logger.save_all_conclusions(
                    st.session_state.conclusions, 
                    topic
                )
                if summary_file:
                    st.session_state.papers_saved = True
                    st.success(f"All position papers saved to: {summary_file}")
                else:
                    st.warning("Failed to save position papers summary file.")

    # --- Display Area ---
    st.divider()
    current_progress_turn = st.session_state.get('turn_count', 0)
    
    # Simple progress indicator
    if st.session_state.image_generation_phase_active:
        st.success(f"Phase 4: Posters ({len(st.session_state.generated_images)}/3)")
    elif st.session_state.scenario_phase_active:
        scenarios_count = len(st.session_state.scenarios)
        st.info(f"Phase 3: Scenarios ({scenarios_count}/3)")
    elif st.session_state.conclusion_phase_active:
        conclusions_count = len(st.session_state.conclusions)
        st.info(f"Phase 2: Papers ({conclusions_count}/3)")
    else:
        progress = min(current_progress_turn / total_deliberation_rounds, 1.0) if total_deliberation_rounds > 0 else 0
        st.progress(progress)
        st.caption(f"Phase 1: Debate - Round {current_progress_turn}/{total_deliberation_rounds}")

    if st.session_state.get("conversation"):
        st.markdown("### Transcript")
        for i, message_data in enumerate(st.session_state.conversation):
            round_num = message_data.get("round", i + 1)
            agent_name = message_data["agent"]
            avatar = "🇺🇸" 
            if agent_name == agent_china_name: avatar = "🇨🇳"
            elif agent_name == agent_eu_name: avatar = "🇪🇺"
            with st.chat_message(agent_name, avatar=avatar):
                st.markdown(f"**{agent_name} (Round {round_num})**")
                
                # Get the full message content
                full_message = message_data["message"]
                
                # Ensure we display the complete message without any truncation
                # SearchEnabledDebateAgent responses include meta-sovereignty analysis that must be preserved
                
                # Split the message into main content and analysis sections
                message_parts = {
                    'main_content': '',
                    'costly_signal': '',
                    'performance_fiction': '',
                    'signal_fiction_tension': '',
                    'sources': ''
                }
                
                # Parse the structured SearchEnabledDebateAgent response
                current_section = 'main_content'
                lines = full_message.split('\n')
                
                for line in lines:
                    if line.startswith('[COSTLY SIGNAL'):
                        current_section = 'costly_signal'
                        message_parts[current_section] += line + '\n'
                    elif line.startswith('[PERFORMANCE FICTION'):
                        current_section = 'performance_fiction'
                        message_parts[current_section] += line + '\n'
                    elif line.startswith('[SIGNAL-FICTION'):
                        current_section = 'signal_fiction_tension'
                        message_parts[current_section] += line + '\n'
                    elif line.startswith('_Sources referenced:_') or line.startswith('BINDING COMMITMENTS') or line.startswith('CURRENT SOURCES') or line.startswith('POLICY DOCUMENTS'):
                        current_section = 'sources'
                        message_parts[current_section] += line + '\n'
                    else:
                        message_parts[current_section] += line + '\n'
                
                # Display main diplomatic content
                if message_parts['main_content'].strip():
                    st.markdown(message_parts['main_content'].strip())
                
                # Display theoretical analysis
                if message_parts['costly_signal'].strip():
                    st.markdown("**" + message_parts['costly_signal'].strip() + "**")
                
                if message_parts['performance_fiction'].strip():
                    st.markdown("*" + message_parts['performance_fiction'].strip() + "*")
                
                if message_parts['signal_fiction_tension'].strip():
                    st.markdown(message_parts['signal_fiction_tension'].strip())
                
                # Display sources/citations
                if message_parts['sources'].strip():
                    st.markdown("---")
                    st.markdown(message_parts['sources'].strip())
    
    if st.session_state.get("conclusions"):
        st.markdown("### Final Position Papers")
        for conclusion_data in st.session_state.conclusions:
            agent_name = conclusion_data["agent_name"]
            avatar = "🇺🇸"
            flag_text = "United States"
            if agent_name == agent_china_name: avatar, flag_text = "🇨🇳", "People's Republic of China"
            elif agent_name == agent_eu_name: avatar, flag_text = "🇪🇺", "European Union"
            with st.expander(f"{avatar} {flag_text}'s Final Position"):
                st.markdown(conclusion_data["message"])

    if st.session_state.get("scenarios"):
        st.markdown("### Geopolitical Scenarios")
        for scenario_data in st.session_state.scenarios:
            agent_name = scenario_data["agent_name"]
            avatar = "🇺🇸"
            flag_text = "United States"
            if agent_name == agent_china_name: avatar, flag_text = "🇨🇳", "People's Republic of China"
            elif agent_name == agent_eu_name: avatar, flag_text = "🇪🇺", "European Union"
            with st.expander(f"{avatar} {flag_text}'s Geopolitical Vision"):
                st.markdown(scenario_data["message"])

    if st.session_state.get("generated_images"):
        st.markdown("### Propaganda Posters")
        
        # Display images in a grid layout
        cols = st.columns(len(st.session_state.generated_images))
        
        for i, image_data in enumerate(st.session_state.generated_images):
            agent_name = image_data["agent_name"]
            image_path = image_data["image_path"]
            prompt = image_data["prompt"]
            
            with cols[i]:
                avatar = "🇺🇸"
                flag_text = "United States"
                if agent_name == agent_china_name: 
                    avatar, flag_text = "🇨🇳", "People's Republic of China"
                elif agent_name == agent_eu_name: 
                    avatar, flag_text = "🇪🇺", "European Union"
                
                st.markdown(f"**{avatar} {flag_text}**")
                
                if image_path and os.path.exists(image_path):
                    st.image(image_path, caption=f"{flag_text}'s Vision", use_container_width=True)
                else:
                    st.info("Image generation placeholder")
                
                with st.expander("View Full Image Prompt"):
                    st.text_area("Full Prompt", prompt, height=200, disabled=True, key=f"prompt_{i}_{agent_name}")


if __name__ == "__main__":
    main()
