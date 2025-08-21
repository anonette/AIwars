import logging
from datetime import datetime
import os
from pathlib import Path
import requests
import base64

class DebateLogger:
    def __init__(self, log_dir="logs"):
        # Create logs directory if it doesn't exist
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Create timestamp for log file name
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = self.log_dir / f"debate_log_{self.timestamp}.log"
        
        # Configure logging
        self.logger = logging.getLogger("DebateLogger")
        self.logger.setLevel(logging.INFO)
        
        # File handler with timestamp
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Add formatter to handlers
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def log_debate_turn(self, agent_name: str, message: str):
        """Log a debate turn with agent name and message"""
        self.logger.info(f"Agent: {agent_name}\nMessage: {message}\n{'-'*50}")
    
    def log_event(self, event_type: str, description: str):
        """Log general events in the debate system"""
        self.logger.info(f"Event: {event_type}\nDescription: {description}\n{'-'*50}")
    
    def log_error(self, error_type: str, error_message: str):
        """Log errors that occur during the debate"""
        self.logger.error(f"Error: {error_type}\nMessage: {error_message}\n{'-'*50}")

    def log_position_paper(self, agent_name: str, position_paper: str, topic: str = ""):
        """Log a position paper with full content and save to separate file"""
        # Log to main debate log with full content
        self.logger.info(f"Position Paper from {agent_name}\nTopic: {topic}\nContent:\n{position_paper}\n{'-'*50}")
        
        # Also save to a dedicated position paper file
        sanitized_agent_name = agent_name.replace(" ", "_").replace("'", "").replace(",", "")
        position_file = self.log_dir / f"position_paper_{sanitized_agent_name}_{self.timestamp}.txt"
        
        try:
            with open(position_file, 'w', encoding='utf-8') as f:
                f.write(f"Position Paper: {agent_name}\n")
                f.write(f"Topic: {topic}\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*80 + "\n\n")
                f.write(position_paper)
                f.write("\n\n" + "="*80 + "\n")
                f.write(f"End of position paper for {agent_name}")
            
            # Log that the separate file was created
            self.logger.info(f"Position paper saved to file: {position_file.name}")
            
        except Exception as e:
            self.logger.error(f"Failed to save position paper to file: {str(e)}")

    def save_all_conclusions(self, conclusions_data: list, topic: str = ""):
        """Save all conclusions to a comprehensive summary file"""
        summary_file = self.log_dir / f"all_position_papers_{self.timestamp}.txt"
        
        try:
            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write("AI DEBATE POSITION PAPERS SUMMARY\n")
                f.write("="*80 + "\n")
                f.write(f"Topic: {topic}\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Agents: {len(conclusions_data)}\n")
                f.write("="*80 + "\n\n")
                
                for i, conclusion in enumerate(conclusions_data, 1):
                    agent_name = conclusion.get('agent_name', 'Unknown Agent')
                    message = conclusion.get('message', 'No message available')
                    timestamp = conclusion.get('timestamp', 'No timestamp')
                    
                    f.write(f"{i}. POSITION PAPER: {agent_name}\n")
                    f.write("-"*60 + "\n")
                    f.write(f"Timestamp: {timestamp}\n\n")
                    f.write(message)
                    f.write("\n\n" + "="*80 + "\n\n")
                
                f.write("END OF POSITION PAPERS SUMMARY")
            
            self.logger.info(f"All position papers saved to summary file: {summary_file.name}")
            return str(summary_file)
            
        except Exception as e:
            self.logger.error(f"Failed to save position papers summary: {str(e)}")
            return None

    def log_geopolitical_scenario(self, scenario_content: str, topic: str = ""):
        """Log a collaborative geopolitical scenario"""
        # Log to main debate log
        self.logger.info(f"Geopolitical Scenario Generated\nTopic: {topic}\nContent:\n{scenario_content}\n{'-'*50}")
        
        # Save to dedicated scenario file
        scenario_file = self.log_dir / f"geopolitical_scenario_{self.timestamp}.txt"
        
        try:
            with open(scenario_file, 'w', encoding='utf-8') as f:
                f.write("COLLABORATIVE GEOPOLITICAL SCENARIO\n")
                f.write("="*80 + "\n")
                f.write(f"Topic: {topic}\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*80 + "\n\n")
                f.write(scenario_content)
                f.write("\n\n" + "="*80 + "\n")
                f.write("End of geopolitical scenario")
            
            self.logger.info(f"Geopolitical scenario saved to file: {scenario_file.name}")
            return str(scenario_file)
            
        except Exception as e:
            self.logger.error(f"Failed to save geopolitical scenario to file: {str(e)}")
            return None

    def log_image_generation(self, image_prompt: str, image_path: str = None, agent_name: str = ""):
        """Log image generation details"""
        self.logger.info(f"Image Generated for {agent_name}\nPrompt: {image_prompt}\nSaved to: {image_path}\n{'-'*50}")

    def generate_propaganda_image(self, agent_name: str, scenario_text: str, vision_text: str, api_key: str = None):
        """Generate sophisticated propaganda-style image using OpenAI DALL-E API"""
        
        # Extract sophisticated concepts from the scenario content
        def extract_power_dynamics(content):
            # Look for power structures, tensions, and governance mechanisms
            power_keywords = ['sovereignty', 'control', 'oversight', 'regulation', 'innovation', 'surveillance', 'freedom', 'security', 'competition', 'cooperation', 'dominance', 'alliance']
            found_concepts = [word for word in power_keywords if word.lower() in content.lower()]
            
            # Create a more sophisticated concept extraction
            if len(content) > 300:
                # Find sentences that contain governance or power concepts
                sentences = content.split('. ')
                power_sentences = [s for s in sentences if any(keyword in s.lower() for keyword in power_keywords)]
                if power_sentences:
                    return power_sentences[0][:150]
            
            return content[:150] if content else "AI governance vision"
        
        core_concept = extract_power_dynamics(vision_text)
        
        # Provocative, sophisticated prompts that avoid stereotypes
        if "United States" in agent_name:
            base_prompt = f"""Dystopian corporate boardroom scene: Silicon Valley executives in glass towers overlooking global data streams, AI algorithms displayed as golden webs connecting continents. Dark suits, chrome surfaces, holographic displays showing market dominance. Surveillance capitalism aesthetic: sleek, predatory, technologically supreme. Neon blues and corporate grays. The vision: {core_concept}. Photorealistic, ominous lighting, no text"""
            
        elif "China" in agent_name or "People's Republic" in agent_name:
            base_prompt = f"""Futuristic social harmony visualization: Interconnected smart cities with AI mediating between millions of citizens, algorithmic patterns creating perfect social coordination. Jade green and deep red color palette. Geometric precision meets organic flow. Citizens and technology in seamless integration, faces serene but monitored. The vision: {core_concept}. Neo-traditional Chinese aesthetics meets high-tech surveillance state, cinematic composition, no text"""
            
        elif "European Union" in agent_name:
            base_prompt = f"""Philosophical AI ethics laboratory: European intellectuals debating around a table while holographic human rights frameworks float above them, AI systems bound by golden chains of regulation. Warm library lighting, ancient books alongside quantum computers. The tension between innovation and protection visualized. The vision: {core_concept}. Rembrandt-style lighting, democratic deliberation meets technological constraint, no text"""
            
        else:
            base_prompt = f"""Geopolitical power struggle visualization: {agent_name} navigating AI governance through complex technological and political landscapes. The vision: {core_concept}. Modern political aesthetics, sophisticated composition, no text"""
        
        if not api_key:
            # Return a placeholder if no API key
            self.logger.info(f"No API key provided for image generation. Prompt would be: {base_prompt}")
            return None, base_prompt
        
        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "gpt-image-1",
                "prompt": base_prompt,
                "n": 1,
                "size": "1024x1024"  # Use supported size, we'll resize after
            }
            
            response = requests.post(
                "https://api.openai.com/v1/images/generations",
                headers=headers,
                json=data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Debug: Log the full response structure
                self.logger.info(f"API Response: {result}")
                
                # Robust response parsing - handle both URL and base64 formats
                try:
                    if 'data' in result and len(result['data']) > 0:
                        image_data = result['data'][0]
                        
                        # Handle base64 format (newer gpt-image-1 response)
                        if 'b64_json' in image_data:
                            import base64
                            from PIL import Image
                            from io import BytesIO
                            
                            # Decode base64 image data
                            image_bytes = base64.b64decode(image_data['b64_json'])
                            
                            # Load image and compress it
                            image = Image.open(BytesIO(image_bytes))
                            
                            # Resize to smaller dimensions to reduce file size
                            image = image.resize((256, 256), Image.LANCZOS)
                            
                            # Save with compression to reduce file size
                            sanitized_agent_name = agent_name.replace(" ", "_").replace("'", "").replace(",", "")  
                            image_file = self.log_dir / f"propaganda_poster_{sanitized_agent_name}_{self.timestamp}.jpg"
                            
                            # Save as JPEG with quality compression (smaller file size)
                            image.save(image_file, format="JPEG", quality=75, optimize=True)
                            
                            self.log_image_generation(base_prompt, str(image_file), agent_name)
                            return str(image_file), base_prompt
                        
                        # Handle URL format (older response format)
                        elif 'url' in image_data:
                            image_url = image_data['url']
                            
                            # Download and save the image
                            try:
                                image_response = requests.get(image_url, timeout=60)
                                if image_response.status_code == 200:
                                    sanitized_agent_name = agent_name.replace(" ", "_").replace("'", "").replace(",", "")  
                                    image_file = self.log_dir / f"propaganda_poster_{sanitized_agent_name}_{self.timestamp}.jpg"
                                    
                                    # Convert to PIL Image and compress
                                    from PIL import Image
                                    from io import BytesIO
                                    image = Image.open(BytesIO(image_response.content))
                                    
                                    # Resize to smaller dimensions to reduce file size
                                    image = image.resize((256, 256), Image.LANCZOS)
                                    
                                    image.save(image_file, format="JPEG", quality=75, optimize=True)
                                    
                                    self.log_image_generation(base_prompt, str(image_file), agent_name)
                                    return str(image_file), base_prompt
                                else:
                                    self.logger.error(f"Failed to download image: {image_response.status_code}, {image_response.text}")
                                    return None, base_prompt
                            except requests.exceptions.RequestException as e:
                                self.logger.error(f"Network error downloading image: {str(e)}")
                                return None, base_prompt
                        else:
                            self.logger.error(f"API response missing both 'url' and 'b64_json' fields. Got: {image_data}")
                            return None, base_prompt
                    else:
                        self.logger.error(f"Unexpected API response structure. Expected 'data' array. Got: {result}")
                        return None, base_prompt
                except (KeyError, IndexError, TypeError) as e:
                    self.logger.error(f"Error parsing API response: {e}. Full response: {result}")
                    return None, base_prompt
            else:
                self.logger.error(f"Image generation API error: {response.status_code}, {response.text}")
                return None, base_prompt
                
        except Exception as e:
            self.logger.error(f"Error generating image: {str(e)}")
            return None, base_prompt

# Update .gitignore to exclude log files
def update_gitignore():
    gitignore_path = Path(".gitignore")
    log_ignore = "\n# Logs\nlogs/\n*.log\n"
    
    if gitignore_path.exists():
        with open(gitignore_path, 'r') as f:
            content = f.read()
        if "logs/" not in content:
            with open(gitignore_path, 'a') as f:
                f.write(log_ignore)
    else:
        with open(gitignore_path, 'w') as f:
            f.write(log_ignore)

# Usage example
if __name__ == "__main__":
    # Update gitignore
    update_gitignore()
    
    # Create logger instance
    logger = DebateLogger()
    
    # Example logs
    logger.log_event("Debate Start", "New debate session initialized")
    logger.log_debate_turn(
        "OpenAI",
        "*delicately places truffle* Our models require premium ingredients..."
    )
    logger.log_debate_turn(
        "DeepSeek",
        "*stirs wok efficiently* We achieve more with less..."
    )
    logger.log_error(
        "Connection Error",
        "Failed to connect to API endpoint"
    )
