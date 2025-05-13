# AI Governance Debate Simulator

A sophisticated debate simulation system that facilitates AI-powered discussions on artificial intelligence governance between virtual representatives of major global powers (United States, European Union, and China).

## Overview

This project simulates high-level diplomatic debates on AI governance and regulation using advanced language models. Each participant represents a major global power and maintains consistent policy positions and negotiation styles aligned with their nation's interests and values.

### Key Features

- **Multi-Agent Debate System**: Simulates interactions between AI representatives from different nations
- **Dynamic Response Generation**: Uses OpenRouter API to access various AI models for generating contextually relevant responses
- **Personality-Driven Interactions**: Each agent maintains a consistent personality and policy stance
- **Structured Debate Format**: Supports multi-round debates with different phases (opening statements, deliberation, conclusion)
- **Real-time Response Generation**: Agents respond to each other's arguments in real-time
- **Fallback Mechanisms**: Includes graceful degradation in case of API failures

## Prerequisites

- Python 3.8+
- OpenRouter API key
- Internet connection for API access

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/AIwars.git
cd AIwars
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with your OpenRouter API key:
```
OPENROUTER_API_KEY=your_api_key_here
```

## Configuration

The system can be configured through `config.yaml`. Key configuration options include:

- Agent personalities and backgrounds
- Model selection for each agent
- Debate parameters (rounds, timing, etc.)
- Custom action sets for each agent

## Usage

1. Start the debate simulation:
```bash
python run_debate.py
```

2. Access the web interface:
   - Open your browser and navigate to the URL shown in the console
   - Default: http://localhost:8501

3. Monitor the debate:
   - Watch agents interact in real-time
   - See their responses and reactions
   - Track debate progress through different rounds

## Debate Structure

The debate follows a structured format:

1. **Opening Round (1-3)**
   - Agents establish their initial positions
   - Present core principles and priorities

2. **Engagement Round (4-7)**
   - Critical discussion of proposals
   - Challenge and defend positions
   - Explore areas of disagreement

3. **Consensus Building (8+)**
   - Work toward common ground
   - Propose compromise solutions
   - Maintain core national interests

4. **Conclusion**
   - Present final position papers
   - Summarize key agreements and disagreements
   - Outline future cooperation frameworks

## Customization

You can customize various aspects of the debate:

- Agent personalities in `config.yaml`
- Debate topics and prompts
- Number of rounds
- Response generation parameters
- UI elements and display options

## Troubleshooting

Common issues and solutions:

1. **API Connection Issues**
   - Verify your OpenRouter API key
   - Check internet connection
   - Confirm API rate limits

2. **Response Generation Failures**
   - System will use fallback responses
   - Check logs for error messages
   - Verify model availability

3. **Performance Issues**
   - Adjust response length limits
   - Modify temperature settings
   - Check system resources

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for:

- Bug fixes
- Feature enhancements
- Documentation improvements
- UI/UX suggestions

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenRouter for API access
- Various AI models used in the system
- Contributors and testers

## Contact

For questions, issues, or suggestions, please open an issue in the repository or contact the maintainers.