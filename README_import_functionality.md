# Import Previous Deliberations & Generate Propaganda Posters

This enhanced feature allows you to import previous AI debate logs and generate propaganda posters from them without re-running the entire simulation.

## 🆕 **Import Functionality**

### 📁 **What You Can Import:**

1. **Position Papers**: Upload `all_position_papers_YYYYMMDD_HHMMSS.txt` files
2. **Geopolitical Scenarios**: Upload `geopolitical_scenario_YYYYMMDD_HHMMSS.txt` files

### 🚀 **How to Use Import Feature:**

1. **Locate Your Log Files**
   ```
   logs/
   ├── all_position_papers_20250607_191452.txt    ← Upload this
   ├── geopolitical_scenario_20250607_191452.txt   ← And/or this
   └── debate_log_20250607_191452.log              (not needed for import)
   ```

2. **Import Process**
   - Go to the **left sidebar** in the Streamlit app
   - Scroll to **"📁 Import Previous Deliberation"** section
   - Upload one or both file types:
     - **Position Papers file** (contains all 3 nation's position papers)
     - **Geopolitical Scenario file** (contains the collaborative scenario)

3. **Process & Generate**
   - Click **"📥 Import & Process Files"**
   - Review the imported content displayed in the main area
   - Click **"🎨 Generate Propaganda Posters from Import"**
   - View the generated propaganda posters!

## 🎨 **Propaganda Poster Generation**

### **What Gets Generated:**
- **🇺🇸 United States**: 1950s patriotic campaign poster style
- **🇪🇺 European Union**: Art Nouveau meets modern design style
- **🇨🇳 China**: Cultural Revolution meets digital art style

### **Image Specifications:**
- **Resolution**: 512x512 pixels (optimized for speed)
- **Format**: PNG files
- **Location**: Saved to `logs/propaganda_poster_[Agent]_YYYYMMDD_HHMMSS.png`

## 🔧 **Technical Details**

### **File Parsing:**
- **Position Papers**: Automatically extracts individual agent positions from summary files
- **Scenarios**: Processes geopolitical scenario content for image generation
- **Agent Mapping**: Intelligently maps agent names to standard formats

### **API Requirements:**
- **For Image Generation**: Requires OpenAI API key (`OPENAI_API_KEY` in `.env`)
- **Fallback Mode**: Shows detailed prompts if no API key available

## 📝 **Example Workflow:**

1. **Run a full debate simulation** to completion
2. **Find your log files** in the `logs/` folder
3. **Start a new session** or use the import feature anytime
4. **Upload the position papers and/or scenario files**
5. **Generate propaganda posters** instantly from past debates!

## ✨ **Benefits:**

- **🔄 Reusability**: Generate images from any past debate
- **⚡ Speed**: Skip the full debate process when you just want images  
- **🎯 Flexibility**: Mix and match different debate outputs
- **📚 Archive**: Build a collection of propaganda posters from different topics
- **🎨 Experimentation**: Try different image settings on the same content

## 🛠️ **Use Cases:**

- **Research**: Generate visual materials for academic presentations
- **Analysis**: Compare different AI governance visions visually
- **Demonstrations**: Show debate outcomes in compelling visual format
- **Collections**: Build galleries of AI governance propaganda across topics
- **Workshops**: Use past debates to generate discussion materials

This import functionality transforms your AI debate simulation into a complete analysis and visualization toolkit! 🎉 