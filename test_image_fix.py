#!/usr/bin/env python3
"""
Test script to validate the image generation fix
"""
import os
from dotenv import load_dotenv
from debate_logger import DebateLogger

# Load environment variables
load_dotenv()

def test_image_generation():
    """Test the fixed image generation functionality"""
    
    # Get API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ No OPENAI_API_KEY found in environment")
        print("Add your OpenAI API key to .env file:")
        print("OPENAI_API_KEY=your_key_here")
        return False
    
    print("✅ OpenAI API key found")
    
    # Create logger instance
    logger = DebateLogger()
    
    # Test image generation for each nation
    test_cases = [
        {
            "agent_name": "United States",
            "scenario_text": "America leads the world in AI innovation through democratic governance and free markets.",
            "vision_text": "Digital freedom and innovation through democratic AI governance"
        },
        {
            "agent_name": "People's Republic of China", 
            "scenario_text": "China achieves harmonious AI development through coordinated governance and social stability.",
            "vision_text": "Harmonious AI development for collective prosperity"
        },
        {
            "agent_name": "European Union",
            "scenario_text": "Europe balances AI innovation with human rights and ethical governance.",
            "vision_text": "Human-centric AI with rights-based governance"
        }
    ]
    
    print(f"\n🧪 Testing image generation with gpt-image-1 model...")
    print("=" * 60)
    
    results = []
    for test_case in test_cases:
        print(f"\n🎨 Generating image for: {test_case['agent_name']}")
        
        try:
            image_path, prompt = logger.generate_propaganda_image(
                agent_name=test_case['agent_name'],
                scenario_text=test_case['scenario_text'],
                vision_text=test_case['vision_text'],
                api_key=api_key
            )
            
            if image_path:
                print(f"✅ SUCCESS: Image saved to {image_path}")
                print(f"📝 Prompt: {prompt[:100]}...")
                results.append({"agent": test_case['agent_name'], "success": True, "path": image_path})
            else:
                print(f"❌ FAILED: No image generated")
                results.append({"agent": test_case['agent_name'], "success": False})
                
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
            results.append({"agent": test_case['agent_name'], "success": False, "error": str(e)})
    
    # Summary
    print("\n" + "=" * 60)
    print("🏁 TEST RESULTS SUMMARY:")
    print("=" * 60)
    
    successes = sum(1 for r in results if r["success"])
    total = len(results)
    
    for result in results:
        status = "✅ SUCCESS" if result["success"] else "❌ FAILED"
        print(f"{result['agent']}: {status}")
        if not result["success"] and "error" in result:
            print(f"   Error: {result['error']}")
        elif result["success"]:
            print(f"   Image: {result['path']}")
    
    print(f"\n📊 Overall: {successes}/{total} images generated successfully")
    
    if successes == total:
        print("🎉 All tests passed! Image generation is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Check the logs above for details.")
        return False

if __name__ == "__main__":
    print("🔧 Testing Image Generation Fix")
    print("Using gpt-image-1 model as specified")
    success = test_image_generation()
    
    if success:
        exit(0)
    else:
        exit(1) 