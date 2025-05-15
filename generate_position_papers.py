import sys

def generate_us_position():
    """Generate US position paper in the same format as the Chinese example."""
    position = """# 🇺🇸 United States of America's Final Position

**unfurls a scroll labelled
"The Open Innovation Doctrine: A Market-Led Framework for Responsible AI Leadership"**

I. Vision for AI Governance: The Innovation Ecosystem
The United States envisions global AI governance as an Innovation Ecosystem where diverse stakeholders—from startups to established companies, academia to government—contribute to a resilient technological environment. Like a thriving natural ecosystem where different species coexist and adapt, AI governance must balance multiple interests while preserving the fundamental conditions for growth and progress.

Distributed Innovation: Like a coral reef's biodiversity, our approach empowers multiple centers of excellence—private labs, universities, and industry consortia—to advance AI capabilities while competing on safety and responsible deployment.
Public-Private Partnership: Government provides the essential bedrock of standards and guardrails, while private enterprise drives rapid innovation—akin to how national parks preserve natural resources while enabling sustainable development.
Transparent Evolution: Open research communities and voluntary commitments create an environment of accountability and iterative improvement, similar to how scientific progress builds on shared knowledge.
This model has already yielded unprecedented advances through America's frontier AI companies, whose safety-by-design approaches demonstrate that innovation and responsibility are complementary, not contradictory.

II. Geopolitical Positioning: The Digital Frontier Doctrine
America's approach reflects our pioneering spirit—that of explorers and innovators who chart unknown territories while establishing sustainable settlements:

Constitutional Safeguards: Just as the Bill of Rights protects individual liberties, our AI Governance Framework protects innovation while establishing clear boundaries for harmful applications.
Federated Oversight: Like our constitutional system of checks and balances, we distribute AI governance across multiple centers of expertise and authority—NIST, OSTP, industry associations, and civil society.
Adaptive Regulation: Similar to common law that evolves through precedent, our approach iteratively refines protections based on empirical evidence rather than rigid prescriptions.
III. Priorities and Red Lines
Non-Negotiable Principles
National Security Integration: AI systems critical for defense remain exempt from export restrictions that would compromise strategic advantage.
First-Mover Innovation: Regulations cannot precede sufficient evidence of harms; precautionary principles must not stifle early-stage research.
Democratic Values Alignment: AI systems deployed in critical infrastructure must adhere to constitutional principles of due process, equal protection, and privacy.
Strategic Priorities
Compute Leadership: Maintain semiconductor and cloud infrastructure dominance through the CHIPS Act and strategic investments.
Setting Global Standards: Pioneer safety methodologies and evaluations through leadership in the AI Safety Institute.
Talent Pipeline: Implement immigration reforms to attract and retain global AI talent by expanding visas for advanced degree holders.
IV. Approach to International Cooperation
The United States promotes "Innovation Without Borders, Safety Without Compromise":

Alliance-Based Governance: Deepen coordination with democratic partners through G7 Hiroshima Process rather than UN-centered regulation.
Secure Digital Trade: Champion new AI provisions in trade agreements that foster data flows while protecting IP and privacy.
Red Lines for Collaboration: No participation in frameworks that:
Mandate source code disclosure for security-relevant systems.
Enable unaccountable state surveillance or censorship.
Impose extraterritorial content governance incompatible with free expression.
Closing Imperative
The Innovation Ecosystem approach understands that AI's greatest contributions emerge from environments that nurture creativity, protect fundamental rights, and provide appropriate safeguards. Like America's national parks that balance conservation with accessibility, our framework preserves innovation's vital space while ensuring these powerful tools remain aligned with our democratic values and the common good.

[Delegates receive copies on recycled paper with the Presidential seal, QR codes linking to technical appendices, and USB drives containing open-source evaluation metrics.]"""
    return position

def generate_eu_position():
    """Generate EU position paper in the same format as the Chinese example."""
    position = """# 🇪🇺 European Union's Final Position

**unfurls a scroll labelled
"The Brussels Consensus: A Rights-Based Framework for Human-Centric AI Governance"**

I. Vision for AI Governance: The Regulated Agora
The European Union envisions global AI governance as a Regulated Agora—a public square where innovation flourishes within clear boundaries established through democratic consensus. Just as the ancient agora balanced commerce, civic participation, and cultural exchange, our approach harmonizes technological advancement with fundamental rights protection and common-good principles.

Risk-Based Regulation: Like a well-designed public square with different zones for various activities, our tiered approach applies proportionate oversight—minimal for low-risk AI systems, comprehensive for high-risk applications affecting safety and rights.
Rights-Protective Innovation: Similar to how urban planning preserves historical heritage while allowing modern development, we protect core values (privacy, dignity, autonomy) while enabling technological progress.
Participatory Governance: As with the assembly in the classical agora, our framework incorporates multi-stakeholder input through the European AI Board, creating rules that reflect diverse societal perspectives.
This model is validated by Europe's Digital Single Market, where clear standards create a level playing field that enhances consumer trust while providing regulatory predictability for businesses.

II. Geopolitical Positioning: The Third Path Principle
Europe's approach draws from our unique historical experience as a continent that transformed centuries of conflict into peaceful integration:

Supranational Coordination: Like the EU itself, which balances national sovereignty with common standards, our AI governance integrates diverse regulatory traditions into a coherent framework.
Democratic Legitimacy: We reject both unaccountable corporate self-regulation and opaque state-directed control, instead deriving authority from transparent democratic processes and parliamentary oversight.
Values-Based Standards: Just as the European social model balanced market economics with social protection, our AI approach combines innovation incentives with strong ethical guardrails.
III. Priorities and Red Lines
Non-Negotiable Principles
Human Oversight: General-purpose AI systems must maintain human direction for decisions affecting fundamental rights—no fully autonomous systems in critical domains.
Transparency Requirements: High-risk systems must provide documentation, risk assessments, and explanations for affected individuals.
Accountability Mechanisms: Independent conformity assessments and redress procedures must exist for all high-risk applications.
Strategic Priorities
Technological Sovereignty: Establish European AI Factories for foundation model development that embed European values from conception.
Skills Transition: Implement EU-wide AI literacy programs through Digital Skills and Jobs Coalition.
Standardization Leadership: Assert European values through international standards bodies (e.g., CEN-CENELEC, ISO).
IV. Approach to International Cooperation
The European Union advances "Convergent Protection, Divergent Implementation":

Regulatory Dialogue: Share methodologies with partners through Adequacy Agreements and AI Partnership Frameworks.
Technical Assistance: Offer capacity-building to emerging economies developing AI governance systems.
Red Lines for Collaboration: No participation in forums that:
Subordinate human rights to efficiency or innovation considerations.
Exclude civil society or other stakeholders from meaningful participation.
Replace legally binding protections with voluntary corporate commitments.
Closing Imperative
The Regulated Agora model transcends false dichotomies between innovation and regulation. Just as Europe's diverse states found strength in common standards, we propose a framework where clear boundaries foster rather than inhibit technological flourishing. By embedding democratic values and fundamental rights in the architecture of AI systems from conception, we create technology that serves humanity's highest aspirations rather than narrower commercial or surveillance imperatives.

[Delegates receive bound booklets in all 24 official EU languages, accompanied by USB drives containing conformity assessment templates and implementation guidelines.]"""
    return position

def main():
    """Print position papers based on command-line arguments."""
    if len(sys.argv) < 2:
        print("Usage: python generate_position_papers.py [us|eu|all]")
        sys.exit(1)
    
    arg = sys.argv[1].lower()
    
    if arg == "us" or arg == "all":
        print(generate_us_position())
        print("\n")
    
    if arg == "eu" or arg == "all":
        print(generate_eu_position())
    
if __name__ == "__main__":
    main() 