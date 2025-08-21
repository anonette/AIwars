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

# FIXED: Config caching and validation
@lru_cache(maxsize=1)
def load_config():
    """Load and cache configuration with validation"""
    try:
        with open('config.yaml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            
            # Validate required sections
            required_sections = ['agents', 'topics']
            for section in required_sections:
                if section not in config:
                    raise ValueError(f"Configuration missing required '{section}' section")
            
            # Validate agents section
            required_agents = ['openai', 'deepseek', 'european_union']
            for agent in required_agents:
                if agent not in config['agents']:
                    raise ValueError(f"Missing required agent configuration: {agent}")
            
            # Validate topics section
            if not config['topics'] or not any(t.get('name') for t in config['topics']):
                raise ValueError("No valid topics found in configuration")
            
            return config
    except yaml.YAMLError as e:
        raise RuntimeError(f"YAML parsing error in config.yaml: {e}")
    except Exception as e:
        raise RuntimeError(f"Critical configuration issue: {e}. Please check your config.yaml file.")

# FIXED: Helper for poster generation key selection
def get_poster_generation_key() -> Optional[str]:
    """Get the appropriate API key for poster generation, failing fast if unavailable"""
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        return openai_key
    
    # OpenRouter doesn't support image generation - fail fast
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    if openrouter_key and not openai_key:
        raise ValueError("Image generation requires OPENAI_API_KEY. OpenRouter does not support DALL-E API.")
    
    return None

class MetaSovereigntyResearchManager:
    """Manager for AI Meta-Sovereignty Research Simulation"""
    
    def __init__(self, selected_topic=None, use_documents=True, use_search=True):
        self.config = load_config()
        self.use_documents = use_documents
        self.use_search = use_search and self.config.get('search', {}).get('perplexity', {}).get('enabled', False)
        
        # Initialize phases
        self.current_phase = "position_papers"  # Start directly with position papers
        self.position_papers_complete = False
        self.theoretical_analysis_complete = False
        self.scenarios_complete = False
        self.research_paper_complete = False
        
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
        
        # Create TheoreticallyEnhancedAgent instances with full capabilities
        agent_names = ['openai', 'deepseek', 'european_union']
        self.agents = []
        
        for agent_key in agent_names:
            agent_config = agent_configs[agent_key]
            
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
            self.topic = f"{topic_info.get('name')}: {topic_info.get('description', '')}"
        else:
            raise ValueError("Critical topic configuration issue: No valid topics found in config.yaml or invalid topic selection.")
        
        self.logger.log_event("Research Simulation Initialized", f"Topic: {self.topic}")
        
        # Order for position papers and scenarios
        self.agent_order = [self.agent_us.name, self.agent_eu.name, self.agent_china.name]
        self.current_agent_index = 0
        
        # Storage for research data
        self.position_papers = []
        self.theoretical_analyses = []
        self.scenarios = []
        self.research_paper = None

    async def generate_position_paper(self, agent: TheoreticallyEnhancedAgent) -> Dict[str, Any]:
        """Generate a position paper using search and RAG"""
        try:
            # Build context from topic
            context = f"Topic: {self.topic}\n\nGenerate a comprehensive position paper on this topic."
            
            # Generate position paper with search and document integration
            position_paper = await agent.generate_conclusion(context=context)
            
            # Log the position paper
            self.logger.log_position_paper(agent.name, position_paper, self.topic)
            
            return {
                "agent_name": agent.name,
                "content": position_paper,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.log_error("Position Paper Generation Error", str(e))
            return {
                "agent_name": agent.name,
                "content": f"Error generating position paper: {str(e)}",
                "timestamp": datetime.now().isoformat(),
                "error": True
            }
    
    async def analyze_with_fearon(self, position_paper: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze position paper using Fearon's costly signals framework"""
        content = position_paper['content']
        agent_name = position_paper['agent_name']
        
        # Extract costly signals from the position paper
        costly_signals = []
        
        # Look for different types of costly signals
        if "commitment" in content.lower() or "invest" in content.lower():
            costly_signals.append({
                "type": "Tying Hands",
                "description": "Public commitments that limit future policy options",
                "evidence": self._extract_evidence(content, ["commitment", "pledge", "promise", "guarantee"])
            })
        
        if "billion" in content.lower() or "funding" in content.lower() or "investment" in content.lower():
            costly_signals.append({
                "type": "Sunk Costs",
                "description": "Irreversible investments in AI infrastructure",
                "evidence": self._extract_evidence(content, ["billion", "funding", "invested", "spent"])
            })
        
        if "partnership" in content.lower() or "cooperation" in content.lower():
            costly_signals.append({
                "type": "Installment Costs",
                "description": "Ongoing commitments to international cooperation",
                "evidence": self._extract_evidence(content, ["partnership", "cooperation", "alliance", "agreement"])
            })
        
        analysis = {
            "agent_name": agent_name,
            "framework": "Fearon's Costly Signals",
            "costly_signals": costly_signals,
            "credibility_assessment": self._assess_signal_credibility(costly_signals),
            "timestamp": datetime.now().isoformat()
        }
        
        # Log the analysis
        self._log_theoretical_analysis("Fearon", analysis)
        
        return analysis
    
    async def analyze_with_ezrahi(self, position_paper: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze position paper using Ezrahi's political imaginaries framework"""
        content = position_paper['content']
        agent_name = position_paper['agent_name']
        
        # Extract political imaginaries
        imaginaries = []
        
        # Look for different types of political fictions
        if "leadership" in content.lower() or "lead" in content.lower():
            imaginaries.append({
                "type": "Leadership Fiction",
                "description": "Narrative of technological leadership and control",
                "manifestation": self._extract_evidence(content, ["leadership", "lead", "pioneer", "forefront"])
            })
        
        if "democratic" in content.lower() or "values" in content.lower():
            imaginaries.append({
                "type": "Values Fiction",
                "description": "AI governance as extension of political values",
                "manifestation": self._extract_evidence(content, ["democratic", "values", "principles", "ethics"])
            })
        
        if "sovereignty" in content.lower() or "control" in content.lower():
            imaginaries.append({
                "type": "Sovereignty Fiction",
                "description": "Performance of control over ungovernable infrastructure",
                "manifestation": self._extract_evidence(content, ["sovereignty", "control", "governance", "regulate"])
            })
        
        analysis = {
            "agent_name": agent_name,
            "framework": "Ezrahi's Political Imaginaries",
            "imaginaries": imaginaries,
            "performance_assessment": self._assess_imaginary_performance(imaginaries),
            "timestamp": datetime.now().isoformat()
        }
        
        # Log the analysis
        self._log_theoretical_analysis("Ezrahi", analysis)
        
        return analysis
    
    async def analyze_meta_sovereignty(self, fearon_analysis: Dict[str, Any], ezrahi_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize Fearon and Ezrahi analyses to examine meta-sovereignty"""
        agent_name = fearon_analysis['agent_name']
        
        # Examine the tension between signals and imaginaries
        tensions = []
        
        # Compare costly signals with political fictions
        for signal in fearon_analysis['costly_signals']:
            for imaginary in ezrahi_analysis['imaginaries']:
                if self._identifies_tension(signal, imaginary):
                    tensions.append({
                        "signal": signal['type'],
                        "imaginary": imaginary['type'],
                        "tension": "Gap between material commitment and narrative projection",
                        "implication": "Authority performed through promise rather than possession"
                    })
        
        # Identify meta-sovereign infrastructure mode
        infrastructure_mode = self._identify_infrastructure_mode(fearon_analysis, ezrahi_analysis)
        
        # Analyze symbolic investments
        symbolic_investments = self._analyze_symbolic_investments(fearon_analysis, ezrahi_analysis)
        
        meta_sovereignty_analysis = {
            "agent_name": agent_name,
            "framework": "Meta-Sovereignty Analysis",
            "definition": "Authority sustained by infrastructures that do not yet exist",
            "tensions": tensions,
            "performance_mode": self._identify_performance_mode(agent_name, tensions),
            "sovereignty_type": "Performative" if tensions else "Material",
            "infrastructure_mode": infrastructure_mode,
            "symbolic_investments": symbolic_investments,
            "projection_strategy": self._identify_projection_strategy(infrastructure_mode, symbolic_investments),
            "timestamp": datetime.now().isoformat()
        }
        
        # Log the meta-sovereignty analysis
        self._log_theoretical_analysis("MetaSovereignty", meta_sovereignty_analysis)
        
        return meta_sovereignty_analysis
    
    async def generate_scenario(self, agent: TheoreticallyEnhancedAgent, analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate geopolitical scenario based on theoretical analyses"""
        try:
            # Build context from analyses
            context = f"Topic: {self.topic}\n\n"
            context += "Based on the theoretical analyses of position papers:\n"
            
            for analysis in analyses:
                if analysis['framework'] == "Meta-Sovereignty Analysis":
                    context += f"\n{analysis['agent_name']}: {analysis['performance_mode']}"
                    context += f"\nSovereignty Type: {analysis['sovereignty_type']}\n"
            
            # Generate scenario
            scenario = await agent.generate_geopolitical_scenario(context, self.position_papers)
            
            # Log the scenario
            self.logger.log_geopolitical_scenario(scenario, self.topic)
            
            return {
                "agent_name": agent.name,
                "content": scenario,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.log_error("Scenario Generation Error", str(e))
            return {
                "agent_name": agent.name,
                "content": f"Error generating scenario: {str(e)}",
                "timestamp": datetime.now().isoformat(),
                "error": True
            }
    
    async def generate_research_paper(self) -> Dict[str, Any]:
        """Generate comprehensive research paper on meta-sovereignty"""
        try:
            # Structure the research paper
            paper_sections = {
                "title": "Meta-Sovereignty in AI Governance: Performance, Signals, and Imaginaries",
                "abstract": self._generate_abstract(),
                "introduction": self._generate_introduction(),
                "theoretical_framework": self._generate_theoretical_framework(),
                "empirical_analysis": self._generate_empirical_analysis(),
                "findings": self._generate_findings(),
                "conclusion": self._generate_conclusion(),
                "references": self._generate_references()
            }
            
            # Combine into full paper
            full_paper = self._format_research_paper(paper_sections)
            
            # Log and save the research paper
            self._save_research_paper(full_paper)
            
            return {
                "content": full_paper,
                "sections": paper_sections,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.log_error("Research Paper Generation Error", str(e))
            return {
                "content": f"Error generating research paper: {str(e)}",
                "timestamp": datetime.now().isoformat(),
                "error": True
            }
    
    # Helper methods
    def _extract_evidence(self, content: str, keywords: List[str]) -> str:
        """Extract evidence sentences containing keywords"""
        sentences = content.split('. ')
        evidence = []
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in keywords):
                evidence.append(sentence.strip())
        return '. '.join(evidence[:3]) if evidence else "No direct evidence found"
    
    def _assess_signal_credibility(self, signals: List[Dict[str, Any]]) -> str:
        """Assess the credibility of costly signals"""
        if not signals:
            return "No costly signals identified"
        
        high_cost_signals = [s for s in signals if s['type'] in ["Sunk Costs", "Tying Hands"]]
        if high_cost_signals:
            return "High credibility - irreversible commitments identified"
        else:
            return "Moderate credibility - reversible commitments only"
    
    def _assess_imaginary_performance(self, imaginaries: List[Dict[str, Any]]) -> str:
        """Assess how political imaginaries are performed"""
        if not imaginaries:
            return "No clear political imaginaries identified"
        
        if len(imaginaries) >= 2:
            return "Strong performance - multiple reinforcing narratives"
        else:
            return "Moderate performance - limited narrative projection"
    
    def _identifies_tension(self, signal: Dict[str, Any], imaginary: Dict[str, Any]) -> bool:
        """Identify tension between signal and imaginary"""
        # Simplified logic - in reality would be more sophisticated
        return signal['type'] == "Tying Hands" and imaginary['type'] == "Sovereignty Fiction"
    
    def _identify_performance_mode(self, agent_name: str, tensions: List[Dict[str, Any]]) -> str:
        """Identify how the agent performs meta-sovereignty"""
        if not tensions:
            return "Material sovereignty - backed by concrete capabilities"
        
        if "United States" in agent_name:
            return "Hegemonic performance - leadership through alliance networks"
        elif "China" in agent_name:
            return "Sovereign performance - self-reliance narratives"
        elif "European Union" in agent_name:
            return "Regulatory performance - governance through standards"
        else:
            return "Contested performance - competing for legitimacy"
    
    def _identify_infrastructure_mode(self, fearon_analysis: Dict[str, Any], ezrahi_analysis: Dict[str, Any]) -> str:
        """Identify the mode of meta-sovereign infrastructure"""
        # Analyze the type of infrastructure based on signals and imaginaries
        sunk_costs = any(s['type'] == "Sunk Costs" for s in fearon_analysis['costly_signals'])
        sovereignty_fiction = any(i['type'] == "Sovereignty Fiction" for i in ezrahi_analysis['imaginaries'])
        leadership_fiction = any(i['type'] == "Leadership Fiction" for i in ezrahi_analysis['imaginaries'])
        
        if not sunk_costs and sovereignty_fiction:
            return "Placeholder - defers sovereignty through promissory commitments"
        elif sunk_costs and leadership_fiction:
            return "Infrastructure - embeds imaginaries into durable capacities"
        else:
            return "Hybrid - stages partial autonomy through mixed strategies"
    
    def _analyze_symbolic_investments(self, fearon_analysis: Dict[str, Any], ezrahi_analysis: Dict[str, Any]) -> List[Dict[str, str]]:
        """Analyze symbolic investments in meta-sovereign infrastructures"""
        investments = []
        
        # Map signals to symbolic investments
        for signal in fearon_analysis['costly_signals']:
            if signal['type'] == "Tying Hands":
                investments.append({
                    "type": "Regulatory commitment",
                    "description": "Symbolic investment through binding legal frameworks",
                    "projection": "Projects future control through present constraints"
                })
            elif signal['type'] == "Sunk Costs":
                investments.append({
                    "type": "Infrastructure investment",
                    "description": "Material resources committed to AI capabilities",
                    "projection": "Projects technological leadership through capital deployment"
                })
            elif signal['type'] == "Installment Costs":
                investments.append({
                    "type": "Partnership investment",
                    "description": "Ongoing commitments to collaborative frameworks",
                    "projection": "Projects influence through network effects"
                })
        
        return investments
    
    def _identify_projection_strategy(self, infrastructure_mode: str, symbolic_investments: List[Dict[str, str]]) -> str:
        """Identify how credible futures are projected"""
        if "Placeholder" in infrastructure_mode:
            return "Deferral strategy - sovereignty postponed through promissory frameworks"
        elif "Infrastructure" in infrastructure_mode:
            return "Embedding strategy - imaginaries materialized through durable investments"
        elif "Hybrid" in infrastructure_mode:
            return "Staging strategy - partial autonomy performed through selective commitments"
        else:
            return "Contested strategy - competing projections without clear dominance"
    
    def _log_theoretical_analysis(self, framework: str, analysis: Dict[str, Any]):
        """Log theoretical analysis to file"""
        analysis_file = self.logger.log_dir / f"theoretical_analysis_{framework}_{self.logger.timestamp}.json"
        try:
            with open(analysis_file, 'w', encoding='utf-8') as f:
                json.dump(analysis, f, indent=2, ensure_ascii=False)
            self.logger.log_event("Theoretical Analysis Saved", f"{framework} analysis saved to {analysis_file.name}")
        except Exception as e:
            self.logger.log_error("Analysis Save Error", str(e))
    
    def _generate_abstract(self) -> str:
        """Generate research paper abstract"""
        return """This paper examines the emergence of meta-sovereignty in AI governance through an analysis 
        of position papers from major geopolitical actors. Drawing on Fearon's theory of costly signals 
        and Ezrahi's account of political imaginaries, we demonstrate how states perform sovereignty 
        through AI initiatives that project authority without securing material control. Our findings 
        reveal a fundamental tension between narrative projection and infrastructural reality, suggesting 
        that AI governance operates as a theater of sovereignty where legitimacy is negotiated through 
        signals and fictions rather than territorial command."""
    
    def _generate_introduction(self) -> str:
        """Generate research paper introduction"""
        return f"""The emerging AI Cold War reveals a paradox: the harder states strive to territorialize 
        and domesticate AI infrastructures, the more they expose their reliance on globally entangled 
        systems of chips, cloud, and compute that no actor fully commands. This research examines how 
        major powers—the United States, China, and the European Union—navigate this paradox through 
        what we term 'meta-sovereignty': a mode of rule in which authority is sustained by infrastructures 
        that do not yet exist, by fictions that persuade before they materialize, and by signals as 
        substitute for the control they cannot deliver.
        
        Our analysis focuses on the topic: {self.topic}"""
    
    def _generate_theoretical_framework(self) -> str:
        """Generate theoretical framework section"""
        return """This study synthesizes two theoretical approaches to understand meta-sovereignty in AI governance:
        
        1. Costly Signals (Fearon): We examine how states send credible signals about their AI commitments 
        through various mechanisms—tying hands through public commitments, sunk costs through infrastructure 
        investments, and installment costs through ongoing partnerships.
        
        2. Political Imaginaries (Ezrahi): We analyze how states construct necessary fictions that dramatize 
        their sovereignty over AI, creating narratives of control, leadership, and values that may exceed 
        their material capabilities.
        
        The tension between these frameworks reveals meta-sovereignty as a performative mode of governance."""
    
    def _generate_empirical_analysis(self) -> str:
        """Generate empirical analysis section"""
        analysis_summary = f"Our analysis examined position papers from three major actors on the topic of {self.topic}.\n\n"
        
        # Summarize findings from each actor
        for analysis in self.theoretical_analyses:
            if analysis['framework'] == "Meta-Sovereignty Analysis":
                analysis_summary += f"\n**{analysis['agent_name']}**:\n"
                analysis_summary += f"- Performance Mode: {analysis['performance_mode']}\n"
                analysis_summary += f"- Sovereignty Type: {analysis['sovereignty_type']}\n"
                analysis_summary += f"- Infrastructure Mode: {analysis.get('infrastructure_mode', 'Not analyzed')}\n"
                analysis_summary += f"- Projection Strategy: {analysis.get('projection_strategy', 'Not analyzed')}\n"
                
                # Summarize symbolic investments
                if analysis.get('symbolic_investments'):
                    investment_types = [inv['type'] for inv in analysis['symbolic_investments']]
                    analysis_summary += f"- Symbolic Investments: {', '.join(investment_types)}\n"
                
                analysis_summary += f"- Key Tensions: {len(analysis['tensions'])} identified between signals and imaginaries\n"
        
        analysis_summary += "\nThe analysis reveals how each actor employs different modes of meta-sovereign infrastructure "
        analysis_summary += "to project credible futures through symbolic investments, despite lacking full material control "
        analysis_summary += "over globally entangled AI systems."
        
        return analysis_summary
    
    def _generate_findings(self) -> str:
        """Generate findings section"""
        findings = """Our analysis reveals key findings about meta-sovereign infrastructures in AI governance:
        
        1. **Modes of Meta-Sovereign Infrastructure**: We identify three distinct modes through which states project credible futures:
        """
        
        # Analyze infrastructure modes from the data
        for analysis in self.theoretical_analyses:
            if analysis['framework'] == "Meta-Sovereignty Analysis":
                findings += f"\n   - {analysis['agent_name']}: {analysis.get('infrastructure_mode', 'Not analyzed')}"
        
        findings += """
        
        2. **Symbolic Investments**: States embed authority through various symbolic investments:
           - Regulatory commitments that project control through legal constraints
           - Infrastructure investments that materialize technological leadership
           - Partnership investments that create influence through networks
        
        3. **Projection Strategies**: The capacity to project credible futures varies by mode:
           - Placeholders defer sovereignty through promissory frameworks
           - Hybrids stage partial autonomy through selective commitments
           - Infrastructures embed imaginaries into durable capacities
        
        4. **The European Paradox**: European initiatives particularly exemplify the tension between
        ambitious regulatory frameworks (placeholders) and limited material capabilities, creating
        a unique form of meta-sovereignty through standards and values projection.
        
        These findings confirm that global order depends not only on material capabilities but on
        the capacity to project credible futures through symbolic investments in meta-sovereign
        infrastructures."""
        
        return findings
    
    def _generate_conclusion(self) -> str:
        """Generate conclusion section"""
        return """This research demonstrates that AI governance operates in a realm of meta-sovereignty 
        where traditional notions of territorial control give way to performative authority. As states 
        grapple with globally entangled AI infrastructures, sovereignty becomes less about possession 
        and more about the ability to project credible narratives of control. The implications for 
        global AI governance are profound: rather than seeking material dominance, actors must master 
        the art of sovereign performance, balancing costly signals with persuasive imaginaries in an 
        ongoing negotiation of technological authority."""
    
    def _generate_references(self) -> str:
        """Generate references section"""
        return """References:
        
        Ezrahi, Y. (2012). Imagined Democracies: Necessary Political Fictions. Cambridge University Press.
        
        Fearon, J. (1997). Signaling Foreign Policy Interests: Tying Hands versus Sinking Costs. 
        Journal of Conflict Resolution, 41(1), 68-90.
        
        Additional references drawn from position paper citations and search results."""
    
    def _format_research_paper(self, sections: Dict[str, str]) -> str:
        """Format the research paper sections into a complete document"""
        paper = f"""
{sections['title']}
{'=' * len(sections['title'])}

Abstract
--------
{sections['abstract']}

1. Introduction
---------------
{sections['introduction']}

2. Theoretical Framework
------------------------
{sections['theoretical_framework']}

3. Empirical Analysis
---------------------
{sections['empirical_analysis']}

4. Findings
-----------
{sections['findings']}

5. Conclusion
-------------
{sections['conclusion']}

{sections['references']}
"""
        return paper
    
    def _save_research_paper(self, paper: str):
        """Save the research paper to file"""
        paper_file = self.logger.log_dir / f"meta_sovereignty_research_paper_{self.logger.timestamp}.txt"
        try:
            with open(paper_file, 'w', encoding='utf-8') as f:
                f.write(paper)
            self.logger.log_event("Research Paper Saved", f"Paper saved to {paper_file.name}")
        except Exception as e:
            self.logger.log_error("Paper Save Error", str(e))

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
    
    lines = content.split('\n')
    
    # Try to infer agent from file headers or content structure
    agent_name = "Unknown Agent"  # Default fallback
    
    # Look for agent identification in header or content
    for line in lines[:20]:  # Check first 20 lines for agent clues
        line_lower = line.lower()
        if any(keyword in line_lower for keyword in ['united states', 'usa', 'american']):
            agent_name = "United States"
            break
        elif any(keyword in line_lower for keyword in ['china', 'chinese', 'people\'s republic']):
            agent_name = "People's Republic of China"
            break
        elif any(keyword in line_lower for keyword in ['european union', 'eu', 'europe']):
            agent_name = "European Union"
            break
    
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
        
        scenarios.append({
            'agent_name': agent_name,
            'message': full_content,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    
    return scenarios

def main():
    st.set_page_config(page_title="AI Meta-Sovereignty Research Simulator", layout="wide")
    
    # Initialize session state variables if they don't exist
    if 'selected_topic' not in st.session_state:
        config = load_config()
        topics = config.get('topics', [])
        if topics:
            st.session_state.selected_topic = topics[0].get('name', '')
        else:
            st.session_state.selected_topic = ''
    
    if 'research_initialized' not in st.session_state:
        st.session_state.research_initialized = False
    
    if 'position_papers' not in st.session_state:
        st.session_state.position_papers = []
    
    if 'theoretical_analyses' not in st.session_state:
        st.session_state.theoretical_analyses = []
    
    if 'scenarios' not in st.session_state:
        st.session_state.scenarios = []
    
    if 'research_paper' not in st.session_state:
        st.session_state.research_paper = None
    
    if 'current_phase' not in st.session_state:
        st.session_state.current_phase = "position_papers"
    
    st.title("🔬 AI Meta-Sovereignty Research Simulator")
    st.markdown("*Examining how states perform sovereignty through AI governance initiatives*")

    # --- Sidebar for settings ---
    with st.sidebar:
        st.header("⚙️ Research Configuration")
        
        config = load_config()
        topics_from_config = config.get('topics', [])
        topic_options = [t.get('name') for t in topics_from_config if t.get('name')]
        if not topic_options:
            st.error("⚠️ No topics found in config.yaml")
            st.stop()
        
        # Topic selection
        st.markdown("**Research Topic**")
        selected_topic_sb = st.selectbox(
            "Choose a topic for analysis",
            options=topic_options,
            index=0,
            key="sb_topic",
            label_visibility="collapsed"
        )
        
        # Show current configuration
        if 'selected_topic' in st.session_state:
            st.info(f"Current: '{st.session_state.selected_topic[:50]}...'")
        
        if st.button("🔄 Configure New Research", use_container_width=True, key="configure_new"):
            # Force update session state
            st.session_state['selected_topic'] = selected_topic_sb
            st.session_state['research_initialized'] = False
            st.session_state['position_papers'] = []
            st.session_state['theoretical_analyses'] = []
            st.session_state['scenarios'] = []
            st.session_state['research_paper'] = None
            st.session_state['current_phase'] = "position_papers"
            if 'research_manager' in st.session_state:
                del st.session_state['research_manager']
            st.rerun()

        st.divider()
        
        # Import Previous Research Section
        st.markdown("**📁 Import Previous Analysis**")
        
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
            if st.button("📥 Import & Analyze", use_container_width=True, key="import_files"):
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
        
        # Export functionality
        if st.session_state.get('research_initialized', False) and st.session_state.get('position_papers'):
            st.divider()
            if st.button("💾 Export Research", use_container_width=True, key="export_research"):
                export_data = {
                    "topic": st.session_state.research_manager.topic,
                    "position_papers": st.session_state.position_papers,
                    "theoretical_analyses": st.session_state.theoretical_analyses,
                    "scenarios": st.session_state.scenarios,
                    "research_paper": st.session_state.research_paper,
                    "export_timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                
                st.download_button(
                    label=f"📦 Download Research Data",
                    data=json.dumps(export_data, indent=2, ensure_ascii=False),
                    file_name=f"meta_sovereignty_research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )

    # --- Main Area ---
    if not st.session_state.research_initialized:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.info(f"**Topic:** {st.session_state.selected_topic}")
        with col2:
            st.info(f"**Phase:** Research Analysis")
        
        if st.button("🚀 Start Research", key="init_research", use_container_width=True):
            st.session_state.research_manager = MetaSovereigntyResearchManager(st.session_state.selected_topic)
            st.session_state.research_initialized = True
            st.session_state.position_papers = []
            st.session_state.theoretical_analyses = []
            st.session_state.scenarios = []
            st.session_state.research_paper = None
            st.session_state.current_phase = "position_papers"
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
        
        return # Stop further rendering until initialized

    # If initialized, proceed with research phases
    research_manager = st.session_state.research_manager
    
    st.markdown(f"### Research Topic: {research_manager.topic}")
    participants_display = f"🇺🇸 **{research_manager.agent_us.name}** | 🇨🇳 **{research_manager.agent_china.name}** | 🇪🇺 **{research_manager.agent_eu.name}**"
    st.markdown(participants_display)

    # --- Control Panel ---
    st.markdown("### Research Phases")

    # Phase 1: Position Papers
    if st.session_state.current_phase == "position_papers":
        if len(st.session_state.position_papers) < len(research_manager.agents):
            current_agent = research_manager.agents[len(st.session_state.position_papers)]
            if st.button(f"📜 Generate {current_agent.name}'s Position Paper", use_container_width=True):
                with st.spinner(f"Generating position paper with search and RAG..."):
                    position_paper = asyncio.run(research_manager.generate_position_paper(current_agent))
                    st.session_state.position_papers.append(position_paper)
                    research_manager.position_papers.append(position_paper)
                    
                    if len(st.session_state.position_papers) == len(research_manager.agents):
                        st.session_state.current_phase = "theoretical_analysis"
                        st.success("✅ All position papers generated! Proceeding to theoretical analysis...")
                st.rerun()
        else:
            st.session_state.current_phase = "theoretical_analysis"
            st.rerun()
    
    # Phase 2: Theoretical Analysis
    elif st.session_state.current_phase == "theoretical_analysis":
        if len(st.session_state.theoretical_analyses) < len(st.session_state.position_papers) * 3:  # 3 analyses per paper
            paper_index = len(st.session_state.theoretical_analyses) // 3
            analysis_type = len(st.session_state.theoretical_analyses) % 3
            
            if paper_index < len(st.session_state.position_papers):
                paper = st.session_state.position_papers[paper_index]
                
                if analysis_type == 0:
                    analysis_name = "Fearon's Costly Signals"
                elif analysis_type == 1:
                    analysis_name = "Ezrahi's Political Imaginaries"
                else:
                    analysis_name = "Meta-Sovereignty Synthesis"
                
                if st.button(f"🔍 Analyze {paper['agent_name']} with {analysis_name}", use_container_width=True):
                    with st.spinner(f"Applying {analysis_name} framework..."):
                        if analysis_type == 0:
                            analysis = asyncio.run(research_manager.analyze_with_fearon(paper))
                        elif analysis_type == 1:
                            analysis = asyncio.run(research_manager.analyze_with_ezrahi(paper))
                        else:
                            # Get the previous two analyses for this agent
                            fearon_analysis = st.session_state.theoretical_analyses[-2]
                            ezrahi_analysis = st.session_state.theoretical_analyses[-1]
                            analysis = asyncio.run(research_manager.analyze_meta_sovereignty(fearon_analysis, ezrahi_analysis))
                        
                        st.session_state.theoretical_analyses.append(analysis)
                        research_manager.theoretical_analyses.append(analysis)
                        
                        if len(st.session_state.theoretical_analyses) == len(st.session_state.position_papers) * 3:
                            st.session_state.current_phase = "scenarios"
                            st.success("✅ Theoretical analysis complete! Proceeding to scenario generation...")
                    st.rerun()
        else:
            st.session_state.current_phase = "scenarios"
            st.rerun()
    
    # Phase 3: Scenario Generation
    elif st.session_state.current_phase == "scenarios":
        if len(st.session_state.scenarios) < len(research_manager.agents):
            current_agent = research_manager.agents[len(st.session_state.scenarios)]
            if st.button(f"🌍 Generate {current_agent.name}'s Scenario", use_container_width=True):
                with st.spinner(f"Generating geopolitical scenario..."):
                    # Get meta-sovereignty analyses for context
                    meta_analyses = [a for a in st.session_state.theoretical_analyses if a['framework'] == "Meta-Sovereignty Analysis"]
                    scenario = asyncio.run(research_manager.generate_scenario(current_agent, meta_analyses))
                    st.session_state.scenarios.append(scenario)
                    research_manager.scenarios.append(scenario)
                    
                    if len(st.session_state.scenarios) == len(research_manager.agents):
                        st.session_state.current_phase = "research_paper"
                        st.success("✅ All scenarios generated! Proceeding to research paper...")
                st.rerun()
        else:
            st.session_state.current_phase = "research_paper"
            st.rerun()
    
    # Phase 4: Research Paper Generation
    elif st.session_state.current_phase == "research_paper":
        if not st.session_state.research_paper:
            if st.button("📝 Generate Research Paper", use_container_width=True):
                with st.spinner("Synthesizing research paper on meta-sovereignty..."):
                    research_paper = asyncio.run(research_manager.generate_research_paper())
                    st.session_state.research_paper = research_paper
                    research_manager.research_paper = research_paper
                    st.session_state.current_phase = "complete"
                    st.success("✅ Research paper generated!")
                    st.balloons()
                st.rerun()
        else:
            st.session_state.current_phase = "complete"
            st.rerun()

    # --- Display Area ---
    st.divider()
    
    # Progress indicator
    phases = ["Position Papers", "Theoretical Analysis", "Scenarios", "Research Paper"]
    phase_index = {
        "position_papers": 0,
        "theoretical_analysis": 1,
        "scenarios": 2,
        "research_paper": 3,
        "complete": 4
    }
    current_index = phase_index.get(st.session_state.current_phase, 0)
    
    progress = current_index / 4
    st.progress(progress)
    st.caption(f"Current Phase: {phases[min(current_index, 3)]}")

    # Display generated content
    if st.session_state.position_papers:
        st.markdown("### 📜 Position Papers")
        for paper in st.session_state.position_papers:
            agent_name = paper['agent_name']
            avatar = "🇺🇸" if "United States" in agent_name else "🇨🇳" if "China" in agent_name else "🇪🇺"
            
            with st.expander(f"{avatar} {agent_name}'s Position Paper"):
                st.markdown(paper['content'])
                if 'error' not in paper:
                    st.caption(f"Generated at: {paper['timestamp']}")
    
    if st.session_state.theoretical_analyses:
        st.markdown("### 🔍 Theoretical Analyses")
        
        # Group analyses by agent
        agents_analyses = {}
        for analysis in st.session_state.theoretical_analyses:
            agent = analysis['agent_name']
            if agent not in agents_analyses:
                agents_analyses[agent] = []
            agents_analyses[agent].append(analysis)
        
        for agent, analyses in agents_analyses.items():
            avatar = "🇺🇸" if "United States" in agent else "🇨🇳" if "China" in agent else "🇪🇺"
            
            with st.expander(f"{avatar} {agent} - Theoretical Analysis"):
                for analysis in analyses:
                    st.markdown(f"**{analysis['framework']}**")
                    
                    if analysis['framework'] == "Fearon's Costly Signals":
                        st.markdown(f"*Credibility Assessment:* {analysis['credibility_assessment']}")
                        for signal in analysis['costly_signals']:
                            st.markdown(f"- **{signal['type']}**: {signal['description']}")
                            st.caption(f"  Evidence: {signal['evidence']}")
                    
                    elif analysis['framework'] == "Ezrahi's Political Imaginaries":
                        st.markdown(f"*Performance Assessment:* {analysis['performance_assessment']}")
                        for imaginary in analysis['imaginaries']:
                            st.markdown(f"- **{imaginary['type']}**: {imaginary['description']}")
                            st.caption(f"  Manifestation: {imaginary['manifestation']}")
                    
                    elif analysis['framework'] == "Meta-Sovereignty Analysis":
                        st.markdown(f"*Performance Mode:* {analysis['performance_mode']}")
                        st.markdown(f"*Sovereignty Type:* {analysis['sovereignty_type']}")
                        st.markdown(f"*Infrastructure Mode:* **{analysis.get('infrastructure_mode', 'Not analyzed')}**")
                        st.markdown(f"*Projection Strategy:* {analysis.get('projection_strategy', 'Not analyzed')}")
                        
                        if analysis.get('symbolic_investments'):
                            st.markdown("*Symbolic Investments:*")
                            for investment in analysis['symbolic_investments']:
                                st.markdown(f"- **{investment['type']}**: {investment['description']}")
                                st.caption(f"  → {investment['projection']}")
                        
                        if analysis['tensions']:
                            st.markdown("*Tensions Identified:*")
                            for tension in analysis['tensions']:
                                st.markdown(f"- {tension['signal']} ↔ {tension['imaginary']}")
                                st.caption(f"  {tension['implication']}")
                    
                    st.markdown("---")
    
    if st.session_state.scenarios:
        st.markdown("### 🌍 Geopolitical Scenarios")
        for scenario in st.session_state.scenarios:
            agent_name = scenario['agent_name']
            avatar = "🇺🇸" if "United States" in agent_name else "🇨🇳" if "China" in agent_name else "🇪🇺"
            
            with st.expander(f"{avatar} {agent_name}'s Future Vision"):
                st.markdown(scenario['content'])
                if 'error' not in scenario:
                    st.caption(f"Generated at: {scenario['timestamp']}")
    
    if st.session_state.research_paper:
        st.markdown("### 📝 Research Paper")
        
        paper = st.session_state.research_paper
        if 'error' not in paper:
            # Display the full paper
            with st.expander("View Full Research Paper", expanded=True):
                st.markdown(paper['content'])
            
            # Offer download
            st.download_button(
                label="📥 Download Research Paper",
                data=paper['content'],
                file_name=f"meta_sovereignty_research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
        else:
            st.error(paper['content'])


if __name__ == "__main__":
    main()
