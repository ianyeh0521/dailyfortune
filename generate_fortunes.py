"""
Fortune Generation Script
Uses OpenAI API to generate approximately 1000 fortune sentences
"""

import json
import os
import time
from typing import List, Dict

try:
    from openai import OpenAI
    OPENAI_V1 = True
except ImportError:
    import openai
    OPENAI_V1 = False

class FortuneGenerator:
    def __init__(self, api_key: str = None):
        """Initialize the fortune generator with OpenAI API key"""
        if OPENAI_V1:
            if api_key:
                self.client = OpenAI(api_key=api_key)
            else:
                # Try to get from environment variable
                self.client = OpenAI()  # Will use OPENAI_API_KEY env var
        else:
            # For older versions of openai library
            if api_key:
                openai.api_key = api_key
            else:
                openai.api_key = os.getenv('OPENAI_API_KEY')
            self.client = None
        
        self.categories = ["encouraging", "motivational", "general", "wisdom", "success", "happiness", "courage", "inspiration"]
        self.generated_fortunes = []
        
    def generate_fortune_batch(self, count: int = 50, category: str = "general") -> List[str]:
        """Generate a batch of fortune sentences"""
        
        prompt = f"""Generate {count} unique, positive fortune cookie messages in the "{category}" category. 
        Each fortune should be:
        - One sentence long
        - Positive and uplifting
        - Between 5-15 words
        - Appropriate for all audiences
        - Unique and not repetitive
        
        Return only the fortune messages, one per line, without numbers or quotes.
        Examples of good fortunes:
        - "Your kindness will be returned to you tenfold"
        - "Today's challenges prepare you for tomorrow's victories"
        - "Success follows those who believe in their dreams"
        """
        
        try:
            if OPENAI_V1:
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a wise fortune cookie writer who creates inspiring, positive messages."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=1000,
                    temperature=0.8
                )
                content = response.choices[0].message.content.strip()
            else:
                # For older versions of openai library
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a wise fortune cookie writer who creates inspiring, positive messages."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=1000,
                    temperature=0.8
                )
                content = response.choices[0].message.content.strip()
            
            fortunes = [line.strip() for line in content.split('\n') if line.strip()]
            
            # Filter out any lines that might be instructions or empty
            fortunes = [f for f in fortunes if len(f.split()) >= 4 and not f.lower().startswith(('here', 'fortune', 'message'))]
            
            return fortunes[:count]  # Ensure we don't exceed the requested count
            
        except Exception as e:
            print(f"Error generating fortunes: {e}")
            return []
    
    def generate_all_fortunes(self, total_count: int = 1000) -> List[Dict]:
        """Generate all fortune sentences across different categories"""
        
        fortunes_per_category = total_count // len(self.categories)
        remaining = total_count % len(self.categories)
        
        all_fortunes = []
        current_id = 21  # Start after existing 20 fortunes
        
        for i, category in enumerate(self.categories):
            count_for_category = fortunes_per_category
            if i < remaining:  # Distribute remainder across first few categories
                count_for_category += 1
                
            print(f"Generating {count_for_category} fortunes for category: {category}")
            
            # Generate in batches of 50 to avoid token limits
            category_fortunes = []
            while len(category_fortunes) < count_for_category:
                batch_size = min(50, count_for_category - len(category_fortunes))
                batch_fortunes = self.generate_fortune_batch(batch_size, category)
                category_fortunes.extend(batch_fortunes)
                
                # Add delay to avoid rate limits
                time.sleep(1)
                
                print(f"Generated {len(category_fortunes)}/{count_for_category} for {category}")
            
            # Convert to fortune objects
            for fortune_text in category_fortunes:
                if fortune_text:  # Skip empty strings
                    all_fortunes.append({
                        "id": current_id,
                        "text": fortune_text,
                        "category": category
                    })
                    current_id += 1
        
        return all_fortunes
    
    def save_fortunes(self, fortunes: List[Dict], filename: str = "new_fortunes.json"):
        """Save generated fortunes to a JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(fortunes, f, indent=2, ensure_ascii=False)
            print(f"Saved {len(fortunes)} fortunes to {filename}")
        except Exception as e:
            print(f"Error saving fortunes: {e}")
    
    def merge_with_existing(self, new_fortunes: List[Dict], existing_file: str = "fortunes.json"):
        """Merge new fortunes with existing ones"""
        existing_fortunes = []
        
        # Load existing fortunes
        if os.path.exists(existing_file):
            try:
                with open(existing_file, 'r', encoding='utf-8') as f:
                    existing_fortunes = json.load(f)
            except Exception as e:
                print(f"Error loading existing fortunes: {e}")
        
        # Combine and save
        all_fortunes = existing_fortunes + new_fortunes
        
        # Create backup of original
        if existing_fortunes:
            backup_file = f"{existing_file}.backup"
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(existing_fortunes, f, indent=2)
            print(f"Created backup: {backup_file}")
        
        # Save merged fortunes
        try:
            with open(existing_file, 'w', encoding='utf-8') as f:
                json.dump(all_fortunes, f, indent=2, ensure_ascii=False)
            print(f"Successfully merged! Total fortunes: {len(all_fortunes)}")
        except Exception as e:
            print(f"Error saving merged fortunes: {e}")

def main():
    """Main function to generate and save fortunes"""
    print("Fortune Generator Starting...")
    print("Make sure you have set your OPENAI_API_KEY environment variable")
    
    try:
        generator = FortuneGenerator()
        
        # Generate ~1000 fortunes
        print("\nGenerating approximately 1000 fortune sentences...")
        new_fortunes = generator.generate_all_fortunes(1000)
        
        if new_fortunes:
            # Save new fortunes separately first
            generator.save_fortunes(new_fortunes, "generated_fortunes.json")
            
            # Merge with existing fortunes
            print("\nMerging with existing fortunes...")
            generator.merge_with_existing(new_fortunes)
            
            print(f"\nComplete! Generated {len(new_fortunes)} new fortunes.")
            print("Files created:")
            print("- generated_fortunes.json (new fortunes only)")
            print("- fortunes.json.backup (backup of original)")
            print("- fortunes.json (merged file with all fortunes)")
        else:
            print("No fortunes were generated. Please check your API key and connection.")
            
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure you have:")
        print("1. Set OPENAI_API_KEY environment variable")
        print("2. Installed openai package: pip install openai==1.52.0")
        print("3. Have sufficient API credits")

if __name__ == "__main__":
    main()