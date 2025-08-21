"""
Log Narrative Transformer
Transforms boring simulation logs into engaging, memorable narratives
"""

import random
import re
from datetime import datetime
from typing import Dict, List, Tuple

class NarrativeTransformer:
    def __init__(self):
        self.characters = self._load_characters()
        self.locations = self._load_locations()
        self.ironies = self._load_ironies()
        self.cultural_details = self._load_cultural_details()
        
    def _load_characters(self) -> Dict[str, List[Dict]]:
        """Load character templates by region"""
        return {
            "China": [
                {"name": "Grandmother Wei", "occupation": "retired teacher", "quirk": "uses AI to cheat at mahjong"},
                {"name": "Li Chen", "occupation": "underground coder", "quirk": "speaks to AI only in Tang poetry"},
                {"name": "Director Zhang", "occupation": "bureaucrat", "quirk": "believes AI can detect sarcasm"},
                {"name": "Xiao Ming", "occupation": "food delivery driver", "quirk": "hacks city brain for faster routes"},
            ],
            "US": [
                {"name": "Brad Thompson", "occupation": "Silicon Valley PM", "quirk": "teaches AI to speak in startup buzzwords"},
                {"name": "Professor Martinez", "occupation": "MIT researcher", "quirk": "accidentally created sentient meme bot"},
                {"name": "Karen Williams", "occupation": "suburban mom", "quirk": "got Alexa to argue with Siri"},
                {"name": "Jake Chen", "occupation": "high school hacker", "quirk": "made GPT write his college essays in iambic pentameter"},
            ],
            "EU": [
                {"name": "Director Van Der Berg", "occupation": "EU bureaucrat", "quirk": "writes regulations longer than Proust"},
                {"name": "Giuseppe Romano", "occupation": "Italian cafe owner", "quirk": "refuses to serve AI-recommended espresso"},
                {"name": "Dr. Müller", "occupation": "German philosopher", "quirk": "debates ethics with chatbots"},
                {"name": "Marie Dubois", "occupation": "French artist", "quirk": "teaches AI to paint with existential dread"},
            ],
            "Africa": [
                {"name": "Amara Okonkwo", "occupation": "startup founder", "quirk": "uses AI to translate venture capitalist BS"},
                {"name": "Professor Tadesse", "occupation": "Ethiopian tech advisor", "quirk": "builds AI that only works during coffee ceremonies"},
                {"name": "Fatima Al-Hassan", "occupation": "Moroccan developer", "quirk": "created AI that argues in three languages simultaneously"},
                {"name": "Joseph Kimani", "occupation": "Kenyan farmer", "quirk": "taught agricultural AI to respect rain prayers"},
            ]
        }
    
    def _load_locations(self) -> Dict[str, List[str]]:
        """Load evocative locations by region"""
        return {
            "China": [
                "a Shanghai tea house where the wifi password changes based on social credit",
                "Beijing's Forbidden City 2.0 (now with 40% more surveillance)",
                "a Shenzhen factory where robots take smoke breaks",
                "an underground bar in Chengdu where VPNs are traded like vintage wine"
            ],
            "US": [
                "a Palo Alto garage where three Stanford dropouts plot digital revolution",
                "Times Square's new AI-powered billboard that reads your emotions",
                "a Texas data center cooled by libertarian hot air",
                "MIT's basement where grad students teach AI to feel impostor syndrome"
            ],
            "EU": [
                "Brussels' Hall of Infinite Regulations",
                "a Parisian cafe where philosophers debate whether AI can experience ennui",
                "Berlin's hackspace decorated with printed GDPR violations",
                "Amsterdam's 'Smart' canal that judges your boat parking"
            ],
            "Global": [
                "the UN's AI Ethics Committee Zoom call (everyone's on mute)",
                "international waters where data laws go to die",
                "a satellite orbiting Earth, laughing at human borders",
                "the internet's basement where deprecated protocols plot revenge"
            ]
        }
    
    def _load_ironies(self) -> List[str]:
        """Load ironic twists and unexpected consequences"""
        return [
            "The AI designed to reduce bureaucracy created seventeen new forms",
            "Privacy-protecting algorithms accidentally made everyone more interesting to advertisers",
            "The harmony-enforcing system caused the Great Passive-Aggressive Uprising of 2025",
            "Efficiency algorithms made meetings 300% longer by optimizing participation",
            "The transparency initiative made everything so transparent no one could see anything",
            "Anti-bias training taught AI to discriminate more creatively",
            "The foolproof security system was defeated by a cat walking on a keyboard",
            "Digital sovereignty meant every country's AI spoke only to itself",
            "The ethics board's AI assistant resigned citing moral objections",
            "Quantum encryption was cracked by asking nicely in binary"
        ]
    
    def _load_cultural_details(self) -> Dict[str, List[str]]:
        """Load cultural flavor text"""
        return {
            "China": [
                "served with jasmine tea and a side of algorithmic harmony",
                "while traditional erhu music played through smart speakers",
                "as the social credit score ticker updated in real-time",
                "beneath portraits of tech leaders practicing tai chi"
            ],
            "US": [
                "while venture capitalists live-tweeted their disruption",
                "as startup founders pivoted mid-sentence",
                "over artisanal coffee and existential dread",
                "while the stock market reacted with emoji"
            ],
            "EU": [
                "after a seventeen-hour discussion on comma placement",
                "while translating regulations into interpretive dance",
                "as bureaucrats formed subcommittees to study the subcommittees",
                "over wine that required blockchain verification"
            ]
        }
    
    def transform_log(self, log_text: str) -> str:
        """Transform a boring log into an engaging narrative"""
        # Extract key information
        title_match = re.search(r'Simulation: (.+?) \((.+?)\)', log_text)
        if title_match:
            original_title = title_match.group(1)
            date = title_match.group(2)
        else:
            original_title = "Unknown Simulation"
            date = "Unknown Date"
        
        # Extract key entities and actions
        entities = self._extract_entities(log_text)
        
        # Generate narrative sections
        narrative_parts = []
        
        # Create engaging title
        new_title = self._generate_title(original_title)
        narrative_parts.append(f"## Simulation: {new_title} ({date})")
        narrative_parts.append(f"*Originally: \"{original_title}\"*\n")
        
        # Add human stories
        for region, actions in entities.items():
            if actions:
                story = self._generate_human_story(region, actions)
                narrative_parts.append(story)
        
        # Add ironic observation
        narrative_parts.append(self._generate_ironic_conclusion())
        
        return "\n".join(narrative_parts)
    
    def _extract_entities(self, log_text: str) -> Dict[str, List[str]]:
        """Extract regions and their actions from log text"""
        entities = {}
        
        # Simple pattern matching for regions
        regions = ["China", "US", "EU", "Ethiopia", "Global South"]
        for region in regions:
            if region in log_text:
                # Extract sentences containing the region
                sentences = log_text.split('.')
                region_actions = [s.strip() for s in sentences if region in s]
                if region_actions:
                    entities[region] = region_actions
        
        return entities
    
    def _generate_title(self, original: str) -> str:
        """Generate a more engaging title"""
        title_templates = [
            "The Great {noun} {crisis}",
            "When {noun} Met {problem}",
            "The {adjective} {noun} Incident",
            "{noun}: A Digital Tragedy in Three Acts",
            "How to Lose {noun} in 10 Days",
            "The {noun} Wars: Episode {number}",
            "Tales from the {noun} Apocalypse"
        ]
        
        # Extract key noun from original
        key_words = original.split()
        noun = next((w for w in key_words if len(w) > 4), "AI")
        
        template = random.choice(title_templates)
        return template.format(
            noun=noun,
            crisis=random.choice(["Crisis", "Debacle", "Fiasco", "Kerfuffle"]),
            adjective=random.choice(["Unexpected", "Hilarious", "Kafkaesque", "Inevitable"]),
            problem=random.choice(["Reality", "Humanity", "Common Sense", "Coffee"]),
            number=random.randint(1, 99)
        )
    
    def _generate_human_story(self, region: str, actions: List[str]) -> str:
        """Generate a human-centered story for a region"""
        # Select appropriate character
        region_key = region if region in self.characters else "US"
        character = random.choice(self.characters.get(region_key, self.characters["US"]))
        
        # Select location
        location_key = region if region in self.locations else "Global"
        location = random.choice(self.locations.get(location_key, self.locations["Global"]))
        
        # Create story
        story_parts = [f"\n### In {location}\n"]
        
        # Add character introduction
        story_parts.append(
            f"{character['name']}, a {character['occupation']} known for their ability to {character['quirk']}, "
            f"discovered that {self._humanize_action(actions[0])}"
        )
        
        # Add cultural detail
        if region in self.cultural_details:
            detail = random.choice(self.cultural_details[region])
            story_parts.append(f" {detail}.")
        
        # Add a quote or reaction
        reaction = self._generate_reaction(character, actions)
        story_parts.append(f"\n\n\"{reaction}\" {character['name']} muttered, {self._generate_action()}.")
        
        return "".join(story_parts)
    
    def _humanize_action(self, action: str) -> str:
        """Convert bureaucratic language to human terms"""
        replacements = {
            "implemented": "forced everyone to use",
            "deployed": "unleashed upon unsuspecting citizens",
            "integrated": "awkwardly shoved together",
            "harmonized": "made to pretend to get along",
            "optimized": "made worse in new and creative ways",
            "leveraged": "exploited",
            "synergized": "created unholy alliance between",
            "framework": "bureaucratic nightmare",
            "ecosystem": "digital zoo",
            "stakeholders": "people with opinions and lawyers"
        }
        
        result = action.lower()
        for old, new in replacements.items():
            result = result.replace(old, new)
        
        return result
    
    def _generate_reaction(self, character: Dict, actions: List[str]) -> str:
        """Generate character reaction"""
        reactions = [
            "Well, this is exactly what Orwell didn't predict",
            "My grandmother's AI is judging me harder than she ever did",
            "I liked it better when computers just played solitaire",
            "The machines aren't taking over - they're just disappointed in us",
            "At least the apocalypse has good wifi",
            "I've seen the future, and it requires a password reset",
            "The singularity arrived, and it's passive-aggressive",
            "We taught AI to think, but forgot to teach it to mind its own business"
        ]
        
        return random.choice(reactions)
    
    def _generate_action(self) -> str:
        """Generate a character action"""
        actions = [
            "updating their VPN for the fifth time today",
            "teaching their smart toaster to be less judgmental",
            "wondering if AI can experience secondhand embarrassment",
            "calculating the social credit cost of this thought",
            "preparing a strongly worded email to the algorithm",
            "considering a career in analog farming",
            "explaining to their AI assistant why it's wrong",
            "nostalgically remembering when privacy was a thing"
        ]
        
        return random.choice(actions)
    
    def _generate_ironic_conclusion(self) -> str:
        """Generate an ironic conclusion"""
        irony = random.choice(self.ironies)
        
        conclusions = [
            f"\n### The Inevitable Irony\n{irony}. Nobody was surprised.",
            f"\n### Plot Twist Nobody Saw Coming (Except Everyone)\n{irony}. The committee to study this phenomenon is still forming subcommittees.",
            f"\n### In Conclusion\n{irony}. This was hailed as a partial success.",
            f"\n### The Real Winner\n{irony}. The AI apologized insincerely."
        ]
        
        return random.choice(conclusions)


def main():
    """Example usage"""
    transformer = NarrativeTransformer()
    
    # Example boring log
    boring_log = """Simulation: Open vs. Closed Source AI (June 11, 2025)
China exported its Three-Layer Regulatory Model to the Global South, embedding algorithmic sovereignty clauses in Digital Silk Road agreements.
US + EU promoted an Alliance for Open AI, framed as "voluntary ethical guidelines" but confined mainly to Western democracies.
Citizens in China used state-approved assistants integrated with social credit-enhanced moderation; Ethiopia's "AI for Harmony" used facial recognition policing."""
    
    # Transform it
    engaging_narrative = transformer.transform_log(boring_log)
    print(engaging_narrative)
    print("\n" + "="*80 + "\n")
    
    # Another example
    boring_log2 = """Simulation: AI Safety Standards (June 16, 2025)
China institutionalized stability-first AI governance via the Shanghai Accord (2032), requiring model registration, algorithmic transparency reports, and data localization.
EU strengthened its "algorithmic audit rights," creating public AI utilities (e.g., EuroMind).
US kept voluntary corporate-driven safeguards, with Apple's "Guide" and Amazon's "Aura" dominating consumer AI but still plagued by filter bubbles and inequality."""
    
    engaging_narrative2 = transformer.transform_log(boring_log2)
    print(engaging_narrative2)


if __name__ == "__main__":
    main()