# Enhanced AI Debate Simulation: Scenario Generation & Propaganda Posters

This enhanced version of the AI debate simulation now includes **creative geopolitical scenario generation** and **propaganda poster creation** after the position papers phase.

## 🆕 New Features

### 🌍 **Phase 3: Geopolitical Scenario Generation**
After all position papers are complete, each AI agent generates a creative geopolitical scenario that describes their ideal AI world 10-20 years in the future.

**What Each Agent Creates:**
- **Detailed future world vision** based on their governance philosophy
- **Specific geopolitical dynamics** and international institutions
- **Citizen experiences** under their AI governance model
- **Concrete examples** of how AI is regulated and deployed
- **Realistic challenges** and how their model overcomes them

### 🎨 **Phase 4: Propaganda Poster Generation**
The final phase generates AI-created propaganda posters in the style of political campaign advertisements for each nation's vision.

**Propaganda Styles:**
- **🇺🇸 United States**: 1950s American campaign posters with stars, stripes, eagles, and tech symbols
- **🇪🇺 European Union**: Art Nouveau meets modern design with EU symbols and democratic themes  
- **🇨🇳 China**: Cultural Revolution meets digital art with red banners and unity themes

## 🔄 Complete Simulation Flow

The enhanced simulation now follows this **4-phase structure**:

1. **🗣️ Phase 1: Deliberation** - Multi-round debate between AI agents
2. **📜 Phase 2: Position Papers** - Formal diplomatic conclusions  
3. **🌍 Phase 3: Geopolitical Scenarios** - Creative future world visions
4. **🎨 Phase 4: Propaganda Posters** - AI-generated campaign imagery

## 🎯 Example Scenarios Generated

Based on our testing, agents create scenarios like:

- **🇺🇸 "The Innovation Archipelago"** - Voluntary networks with distributed oversight
- **🇪🇺 "The Rights-Based Digital Confederation"** - Binding treaties with human rights focus
- **🇨🇳 "The Coordinated Prosperity Initiative"** - Comprehensive governance for social stability

## 📁 Enhanced File Structure

The system now creates additional files in the `logs/` directory:

```
logs/
├── debate_log_YYYYMMDD_HHMMSS.log                    # Main debate log
├── position_paper_[Agent]_YYYYMMDD_HHMMSS.txt        # Individual position papers
├── all_position_papers_YYYYMMDD_HHMMSS.txt           # All position papers summary
├── geopolitical_scenario_YYYYMMDD_HHMMSS.txt         # Collaborative scenario file
├── propaganda_poster_[Agent]_YYYYMMDD_HHMMSS.png     # Generated propaganda images
└── all_scenarios_YYYYMMDD_HHMMSS.txt                 # All scenarios summary
```

## 🛠️ Technical Implementation

### New Methods Added:
- `DebateAgent.generate_geopolitical_scenario()` - Creates future world scenarios
- `DebateLogger.log_geopolitical_scenario()` - Saves scenario content
- `DebateLogger.generate_propaganda_image()` - Creates AI images via DALL-E API

### API Requirements:
- **Position Papers & Scenarios**: Uses your existing OpenRouter API key
- **Image Generation**: Uses OpenAI DALL-E API (same API key if you have OpenAI access)

## 🚀 How to Use the Enhanced Features

1. **Run your debate simulation** as usual: `python run_debate.py`
2. **Complete all deliberation rounds** and position papers
3. **Click "🌍 Proceed to Scenario Generation Phase"** when prompted
4. **Generate each agent's geopolitical scenario** using the buttons
5. **Click "🎨 Generate Propaganda Posters"** to create campaign images
6. **View the results** in the web interface and check the `logs/` folder

## 🎨 Image Generation Notes

- **With API Key**: Real propaganda posters are generated and saved as PNG files
- **Without API Key**: Shows what would be generated with detailed prompts
- **Fallback Mode**: System works even if image generation fails

## 📊 Enhanced Progress Display

The UI now shows a **4-phase progress tracker**:
- 🗣️ Phase 1/4: Deliberation - Round X of Y
- 📜 Phase 2/4: Position Papers (X/3)  
- 🌍 Phase 3/4: Geopolitical Scenarios (X/3)
- 🎨 Phase 4/4: Propaganda Posters Generated (X/3)

## 🎉 Final Result

When complete, you'll have:
- **Complete debate transcript** with all rounds
- **3 formal position papers** in diplomatic style  
- **3 creative geopolitical scenarios** describing ideal AI futures
- **3 propaganda posters** visualizing each nation's vision
- **Comprehensive logs** with everything saved for analysis

This creates a **complete AI governance simulation** from initial debate through final visual propaganda, offering insights into how different AI governance philosophies might play out in the real world! 