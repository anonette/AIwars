import streamlit as st
from debate_manager import DebateManager
from debate_system import DebateAgent
import asyncio
import json
import yaml
from datetime import datetime
from debate_logger import DebateLogger
import re

def load_config():
    try:
        with open('config.yaml', 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading config: {e}")
        return {}

class StreamlitDebateManager:
    def __init__(self, selected_topic=None, total_rounds=20):
        # Load config
        self.config = load_config()
        self.debate_prompt = self.config.get('debate_prompt', '')
        self.total_rounds = total_rounds
        self.conclusion_phase = False
        
        # Get agent configurations from config
        agent_configs = self.config.get('agents', {})
        
        # Initialize debate agents with names and personalities from config
        self.agent_us = DebateAgent(
            name=agent_configs['openai']['name'],
            personality=agent_configs['openai']['personality'],
            config=self.config
        )
        
        self.agent_china = DebateAgent(
            name=agent_configs['deepseek']['name'],
            personality=agent_configs['deepseek']['personality'],
            config=self.config
        )
        
        self.agent_eu = DebateAgent(
            name=agent_configs['european_union']['name'],
            personality=agent_configs['european_union']['personality'],
            config=self.config
        )
        
        self.agents = [self.agent_us, self.agent_china, self.agent_eu]
        
        self.logger = DebateLogger()
        
        # Get topic (use selected or random)
        topics = self.config.get('topics', [])
        
        # Filter for EU scenario topics if no specific topic selected
        if not selected_topic:
            scenario_topics = [t for t in topics if any(s in t.get('name', '') 
                                                      for s in ['Machinic', 'Technocratic', 'Infrastructural', 'Digital Non-Alignment'])]
            
            # Default to the EU scenario topics, or full topic list if none found
            topics_to_choose_from = scenario_topics if scenario_topics else topics
            
            import random
            topic_obj = random.choice(topics_to_choose_from)
            topic = topic_obj.get('name', "Future EU AI Governance")
        else:
            topic = selected_topic
        
        # Initialize debate manager with list of agents
        self.debate = DebateManager(
            agents=self.agents,
            topic=topic
        )
        self.logger.log_event("Deliberation Initialized", f"Topic: {self.debate.topic}, Rounds: {self.total_rounds}")
        self.current_round = 0
        
        # Track which agents have given their conclusion
        self.conclusion_sequence = []  # Will contain tuples of (agent_name, scenario_name)
        
        # Define specific conclusion scenarios for each agent
        self.conclusion_scenarios = {
            self.agent_us.name: {
                "title": "The Innovation Archipelago Scenario",
                "metaphor": "Frontier/Maritime Law",
                "document": "The Digital Frontiersman"
            },
            self.agent_china.name: {
                "title": "The Ordered Prosperity Scenario",
                "metaphor": "Silk Road",
                "document": "The Harmonious Cultivation"
            },
            self.agent_eu.name: {
                "title": "The Balanced Integration Scenario",
                "metaphor": "Agora/Postwar Consensus",
                "document": "The Digital Agora"
            }
        }
        
        # Define the sequence for conclusion presentations
        self.conclusion_order = [
            self.agent_us.name,
            self.agent_eu.name,
            self.agent_china.name
        ]
        
        self.current_conclusion_index = 0

    async def get_next_response(self):
        # Check if we've reached the conclusion phase
        if self.current_round >= self.total_rounds and not self.conclusion_phase:
            self.conclusion_phase = True
            self.current_round = 0  # Reset for conclusion tracking
            return self._prepare_conclusion_transition()
            
        # In conclusion phase, provide pre-defined conclusions in sequence
        if self.conclusion_phase:
            # Check if we've presented all conclusions
            if self.current_conclusion_index >= len(self.conclusion_order):
                return None
                
            # Get the next agent in the conclusion sequence
            agent_name = self.conclusion_order[self.current_conclusion_index]
            self.current_conclusion_index += 1
            
            # Get the conclusion for this agent
            conclusion = self._get_agent_conclusion(agent_name)
            
            # Log the conclusion
            self.logger.log_event(f"Conclusion from {agent_name}", 
                                 f"Scenario: {self.conclusion_scenarios[agent_name]['title']}")
            
            return {
                "agent_name": agent_name,
                "message": conclusion
            }
        
        # Regular deliberation phase
        # Increment round counter for non-first messages
        if self.debate.conversation_history:
            self.current_round += 1
        
        # Create a formatted debate prompt with round information
        round_info_prompt = self.debate_prompt.replace(
            "{round_number}", str(self.current_round + 1)
        ).replace(
            "{total_rounds}", str(self.total_rounds)
        )
        
        # Start debate or get next turn
        if not self.debate.conversation_history:
            response = await self.debate.start_debate(debate_prompt=round_info_prompt)
            self.logger.log_event("Deliberation Started", f"Round 1 of {self.total_rounds}")
            self.current_round = 1
        else:
            response = await self.debate.next_turn(debate_prompt=round_info_prompt)
            self.logger.log_event(f"Deliberation Round {self.current_round}", 
                                f"Agent: {self.debate.get_current_agent_name()}")
            
        return response
    
    def _prepare_conclusion_transition(self):
        """Create a transition message to the conclusion phase"""
        return f"After {self.total_rounds} rounds of deliberation on {self.debate.topic}, " + \
               "each representative will now present their final position and vision for the future of AI governance."
    
    def _get_agent_conclusion(self, agent_name):
        """Get the pre-defined conclusion for the specified agent"""
        scenario = self.conclusion_scenarios[agent_name]
        
        if agent_name == self.agent_us.name:
            return f"""*presents "{scenario['document']}" position paper*

**{scenario['title']}**

The United States envisions an AI future characterized by what we call the "{scenario['title']}" - a dynamic ecosystem of interconnected but independent technology hubs, linked through voluntary standards but preserving the creative freedom essential for breakthrough innovations. Like the historic frontier that shaped American identity, this digital frontier rewards bold exploration while maintaining strategic outposts of security oversight only where genuinely needed.

In geopolitical terms, we see AI governance as analogous to maritime law - providing freedom of navigation in the digital commons while asserting specific sovereign rights in critical security domains. Just as naval power historically secured trade routes while enabling exploration, our approach secures essential technology pathways while enabling maximum innovation potential.

Key priorities: Maintaining technological leadership, protecting national security, fostering innovation ecosystems, and developing voluntary risk management frameworks. Our red lines include restrictions that disproportionately impact U.S. competitiveness or military applications essential for defense.

The United States remains committed to international cooperation through the G7 AI Process, OECD frameworks, and bilateral technology alliances, while ensuring any global standards preserve the innovation potential that drives economic growth and democratic values.
"""
        elif agent_name == self.agent_eu.name:
            return f"""*presents "{scenario['document']}" framework document*

**{scenario['title']}**

The European Union's vision centers on what we call the "{scenario['title']}" - a carefully architected AI ecosystem where technological capabilities and democratic values form a mutually reinforcing structure. Like the ancient Greek agora that served as marketplace, civic center, and forum simultaneously, our AI framework creates a space where innovation, rights protection, and public discourse coexist in productive tension.

In geopolitical terms, we see our position as analogous to the European postwar consensus - recognizing that legitimate commercial interests and fundamental democratic principles must be bound together through enforceable standards with clear accountability mechanisms. Just as the European project balanced national sovereignty with shared values, our approach to AI balances technological advancement with human dignity.

Key priorities: Risk-based regulation, fundamental rights protection, technological sovereignty, data governance based on European values, and preventing infrastructural dependencies. Our red lines include unaccountable AI systems, compromised democratic processes, and technological lock-in to non-European platforms.

We remain committed to multilateral cooperation through binding international frameworks, but insist these must include meaningful accountability mechanisms that preserve the democratic control of technology and human dignity as non-negotiable principles.
"""
        else:  # China
            return f"""*presents "{scenario['document']}" strategic document*

**{scenario['title']}**

China's vision for AI governance follows what we term the "{scenario['title']}" - a coordinated development path where technological advancement is deliberately cultivated to serve strategic national objectives and social harmony. Like a carefully tended garden that requires both structure and nurturing, our approach provides the necessary frameworks to guide AI toward socially beneficial outcomes through disciplined implementation.

In geopolitical terms, our approach resembles the ancient Silk Road - a structured network of technological exchange that respects territorial sovereignty while enabling strategic flows of innovation under coordinated oversight. Just as the historical Silk Road facilitated trade while maintaining imperial administration, our model enables technological advancement while preserving sovereign control over its implementation.

Key priorities: Technological autonomy, social stability, algorithmic governance frameworks, strategic international standards setting, and maintaining sovereignty over data infrastructure. Our red lines include interference in domestic governance approaches and inequitable access to advanced technology resources.

China supports international cooperation on AI governance through the Global AI Governance Initiative while respecting different national conditions, opposing technological hegemony, and ensuring representation of diverse governance models in international standard-setting bodies.
"""
    
    def _build_conclusion_context(self):
        """Build context from the full conversation history for conclusion"""
        if not self.debate.conversation_history:
            return f"Topic: {self.debate.topic}"
            
        # Include more context for conclusions
        return "\n".join([f"{msg['agent']}: {msg['message']}"
                        for msg in self.debate.conversation_history[-10:]])

def get_scenario_description(topic):
    """Get a detailed description for EU scenarios"""
    scenarios = {
        "Machinic Federation": """
        In the Machinic Federation scenario, Europe embraces decentralized algorithmic governance systems 
        that operate with significant autonomy. This future envisions a federation where algorithms and 
        automated systems manage many governance functions with minimal human intervention, creating 
        a distributed form of sovereignty spread across multiple computational nodes.
        
        Key characteristics:
        - Highly automated decision-making systems with algorithmic accountability
        - Decentralized technical architecture with distributed governance
        - Advanced federated learning across sovereign nodes
        - Complex balance between autonomy and human oversight
        """,
        
        "Technocratic Fortress": """
        The Technocratic Fortress scenario presents Europe as a regulatory superpower that has achieved 
        technological self-sufficiency through stringent controls and massive public investment. 
        In this future, Europe has built its own technological stack and regulatory regime that operates 
        independently from other global powers.
        
        Key characteristics:
        - Comprehensive regulatory frameworks with strong enforcement mechanisms
        - Technological sovereignty through domestic capabilities
        - State-directed AI development with strategic industrial policy
        - High barriers to external technological influence
        """,
        
        "Infrastructural Vassalage": """
        In the Infrastructural Vassalage scenario, Europe has become dependent on external technological 
        infrastructure, limiting its regulatory autonomy and strategic independence. Though maintaining 
        formal sovereignty, Europe's practical ability to govern technology is constrained by its 
        reliance on systems controlled by other powers.
        
        Key characteristics:
        - Critical technology dependence on external providers
        - Limited enforcement capacity for domestic regulations
        - Regulatory initiatives undermined by infrastructure dependencies
        - Diminished strategic autonomy in technology governance
        """,
        
        "Digital Non-Alignment": """
        The Digital Non-Alignment scenario depicts Europe pursuing a strategic middle path between 
        competing technological ecosystems. Rather than fully aligning with any single global power, 
        Europe maintains selective engagement and compatibility with multiple systems while preserving 
        core sovereignty through strategic technological capabilities.
        
        Key characteristics:
        - Balanced approach to technology partnerships and standards
        - Strategic technological independence in critical domains
        - Interoperability with multiple global systems
        - Diplomatic leadership in multilateral governance forums
        """
    }
    
    # Look for scenario name in topic
    for scenario in scenarios:
        if scenario in topic:
            return scenarios[scenario]
    
    return "Selected scenario explores how European technological sovereignty might be enacted within contested post-sovereign infrastructures."

def format_message_with_round(message, round_num=None):
    """Format a message with round information if available"""
    if round_num:
        # Add round information at the beginning
        return f"**Round {round_num}**\n\n{message}"
    return message

def load_conversation_history():
    with open('debate_conversation.json', 'r') as f:
        return json.load(f)

def main():
    st.set_page_config(page_title="AI Futures Deliberation", layout="wide")
    
    # Title and description
    st.title("🌐 AI Futures Deliberation")
    st.markdown("A deliberative simulation of strategic AI governance scenarios and their implications for digital sovereignty")
    
    # Sidebar for settings
    with st.sidebar:
        st.subheader("Deliberation Settings")
        
        # Topic selection focusing on EU scenarios
        config = load_config()
        topics = config.get('topics', [])
        
        # Filter for EU scenario topics
        scenario_topics = [t for t in topics if any(s in t.get('name', '') 
                                                  for s in ['Machinic', 'Technocratic', 'Infrastructural', 'Digital Non-Alignment'])]
        
        # Default to scenario topics or full list if none found
        topic_options = [t.get('name') for t in (scenario_topics if scenario_topics else topics)]
        
        selected_topic = st.selectbox(
            "Select Scenario", 
            options=topic_options,
            index=0 if topic_options else 0
        )
        
        # Number of deliberation rounds
        num_rounds = st.slider("Deliberation Rounds", min_value=10, max_value=20, value=20)
        
        # Control buttons
        if st.button("🔄 Start New Deliberation", use_container_width=True):
            st.session_state.conversation = []
            st.session_state.turn_count = 0
            st.session_state.conclusions = []
            st.session_state.debate_manager = StreamlitDebateManager(selected_topic, num_rounds)
            st.session_state.scenario_description = get_scenario_description(selected_topic)
            st.rerun()
            
        if 'turn_count' in st.session_state and st.session_state.turn_count > 0:
            if st.button("📝 Export Deliberation", use_container_width=True):
                # Logic to export deliberation results
                export_data = {
                    "deliberation": st.session_state.conversation,
                    "conclusions": st.session_state.get("conclusions", [])
                }
                st.download_button(
                    label="Download Transcript",
                    data=json.dumps(export_data, indent=2),
                    file_name=f"deliberation_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                    mime="application/json"
                )
    
    # Main content area
    if 'debate_manager' not in st.session_state:
        st.session_state.debate_manager = StreamlitDebateManager(selected_topic, num_rounds)
        st.session_state.scenario_description = get_scenario_description(selected_topic)
    
    debate_manager = st.session_state.debate_manager
    agent_us_name = debate_manager.agent_us.name
    agent_china_name = debate_manager.agent_china.name
    agent_eu_name = debate_manager.agent_eu.name
    topic = debate_manager.debate.topic
    
    # Display scenario description and context
    st.markdown(f"### Scenario: {topic}")
    st.markdown(st.session_state.scenario_description)
    
    st.markdown("### Participants")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"**{agent_us_name}** 🇺🇸")
        st.caption("*Voluntary safeguards and innovation-first approach*")
    
    with col2:
        st.markdown(f"**{agent_china_name}** 🇨🇳")
        st.caption("*Centralized control and algorithmic governance*")
    
    with col3:
        st.markdown(f"**{agent_eu_name}** 🇪🇺")
        st.caption("*Excellence and trust with balanced regulation*")
    
    # Initialize conversation and conclusions state
    if 'conversation' not in st.session_state:
        st.session_state.conversation = []
    
    if 'conclusions' not in st.session_state:
        st.session_state.conclusions = []
    
    # Progress bar and phase indicator
    if 'turn_count' in st.session_state:
        if debate_manager.conclusion_phase:
            # Show conclusion phase indicator
            st.success(f"Deliberation complete! ({st.session_state.turn_count} rounds) - Now in conclusion phase")
            progress = 1.0  # Full progress
        else:
            # Show deliberation progress
            progress = min(st.session_state.turn_count / debate_manager.total_rounds, 1.0)
            st.progress(progress)
            st.caption(f"Deliberation Progress: Round {st.session_state.turn_count} of {debate_manager.total_rounds}")
    
    # Display main deliberation transcript
    if not debate_manager.conclusion_phase or len(st.session_state.conversation) > 0:
        st.markdown("### Deliberation Transcript")
        
        for i, message in enumerate(st.session_state.conversation):
            round_num = i + 1
            avatar = "🇺🇸"
            if message["agent"] == agent_china_name:
                avatar = "🇨🇳"
            elif message["agent"] == agent_eu_name:
                avatar = "🇪🇺"
                
            with st.chat_message(
                message["agent"],
                avatar=avatar
            ):
                # Format message with round number
                formatted_message = format_message_with_round(message["message"], round_num)
                st.markdown(f"**{message['agent']} (Round {round_num})**")
                st.markdown(formatted_message)
    
    # Display conclusions if available
    if st.session_state.get("conclusions", []):
        st.markdown("### Final Position Papers")
        
        # Define the correct agent names for matching
        us_agent_name = agent_us_name  # "United States"
        china_agent_name = agent_china_name  # "People's Republic of China"
        eu_agent_name = agent_eu_name  # "European Union"
        
        for conclusion in st.session_state.conclusions:
            agent_name = conclusion["agent_name"]
            
            # Debug output to see what's happening
            st.text(f"Debug - Agent name in conclusion: {agent_name}")
            st.text(f"Debug - Expected US: {us_agent_name}, China: {china_agent_name}, EU: {eu_agent_name}")
            
            avatar = "🇺🇸"
            flag_text = "United States"
            
            # Exact string comparison for agent names
            if agent_name == china_agent_name:
                avatar = "🇨🇳"
                flag_text = "People's Republic of China"
            elif agent_name == eu_agent_name:
                avatar = "🇪🇺"
                flag_text = "European Union"
            elif agent_name == us_agent_name:
                avatar = "🇺🇸"
                flag_text = "United States"
                
            with st.expander(f"{avatar} {flag_text} Final Position"):
                st.markdown(conclusion["message"])
    
    # Automatically generate responses
    if 'turn_count' not in st.session_state:
        st.session_state.turn_count = 0

    # Continue generating content
    if st.session_state.turn_count < debate_manager.total_rounds or debate_manager.conclusion_phase:
        with st.spinner(f"Generating {'conclusion' if debate_manager.conclusion_phase else f'round {st.session_state.turn_count + 1}'}..."):
            response = asyncio.run(st.session_state.debate_manager.get_next_response())
            
            # Skip if no response (happens after all conclusions are done)
            if response is None:
                st.success("Deliberation and conclusions complete!")
                st.stop()
            
            # Handle transition message
            if isinstance(response, str):
                st.info(response)
                st.rerun()
                
            # Normal response processing
            if debate_manager.conclusion_phase:
                # In conclusion phase, response is a dictionary with agent_name and message
                current_agent = response["agent_name"]
                message = response["message"]
                
                st.text(f"Debug - Adding conclusion from: {current_agent}")
                
                st.session_state.conclusions.append({
                    "agent_name": current_agent,
                    "message": message,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
            else:
                # In regular phase, response is just the message
                current_agent = st.session_state.debate_manager.debate.get_current_agent_name()
                message = response
                
                st.session_state.conversation.append({
                    "agent": current_agent,
                    "message": message,
                    "round": st.session_state.turn_count + 1,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                st.session_state.turn_count += 1
            
            # Log the response
            st.session_state.debate_manager.logger.log_debate_turn(current_agent, message)
            st.rerun()
    else:
        # Trigger conclusion phase if deliberation complete but conclusions not started
        if not debate_manager.conclusion_phase:
            st.session_state.debate_manager.conclusion_phase = True
            st.rerun()

if __name__ == "__main__":
    main()
