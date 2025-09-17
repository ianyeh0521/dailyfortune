"""
Fortune Data Management
Handles fortune storage, user history, and daily limit logic
"""

import json
import os
import random
from datetime import datetime, date
from typing import Dict, List, Optional

class FortuneManager:
    def __init__(self):
        self.app_dir = os.path.expanduser("~/.dailyfortune")
        os.makedirs(self.app_dir, exist_ok=True)
        
        # Handle both development and PyInstaller bundle
        import sys
        if getattr(sys, 'frozen', False):
            # Running as PyInstaller bundle
            bundle_dir = sys._MEIPASS
            self.fortunes_file = os.path.join(bundle_dir, "fortunes.json")
        else:
            # Running as script
            self.fortunes_file = os.path.join(os.path.dirname(__file__), "fortunes.json")
        self.user_data_file = os.path.join(self.app_dir, "user_data.json")
        
        self.fortunes = self._load_fortunes()
        self.user_data = self._load_user_data()
    
    def _load_fortunes(self) -> List[Dict]:
        """Load fortune database"""
        try:
            if os.path.exists(self.fortunes_file):
                with open(self.fortunes_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading fortunes: {e}")
        
        # Default fortunes if file doesn't exist
        return self._create_default_fortunes()
    
    def _create_default_fortunes(self) -> List[Dict]:
        """Create default fortune set"""
        return [
            {"id": 1, "text": "Today brings new opportunities your way", "category": "encouraging"},
            {"id": 2, "text": "Your patience will be rewarded soon", "category": "motivational"},
            {"id": 3, "text": "A small act of kindness will make a big difference", "category": "general"},
            {"id": 4, "text": "Trust your instincts today", "category": "encouraging"},
            {"id": 5, "text": "Good things come to those who wait", "category": "motivational"},
            {"id": 6, "text": "You are stronger than you think", "category": "encouraging"},
            {"id": 7, "text": "Today is a perfect day to start something new", "category": "motivational"},
            {"id": 8, "text": "The best is yet to come", "category": "encouraging"},
            {"id": 9, "text": "Your hard work will pay off", "category": "motivational"},
            {"id": 10, "text": "Believe in yourself and magic will happen", "category": "encouraging"}
        ]
    
    def _load_user_data(self) -> Dict:
        """Load user history and data"""
        try:
            if os.path.exists(self.user_data_file):
                with open(self.user_data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading user data: {e}")
        
        return {
            "device_id": self._generate_device_id(),
            "history": []
        }
    
    def _generate_device_id(self) -> str:
        """Generate unique device identifier"""
        import platform
        import hashlib
        
        system_info = f"{platform.system()}-{platform.node()}-{platform.processor()}"
        return hashlib.md5(system_info.encode()).hexdigest()[:16]
    
    def _save_user_data(self):
        """Save user data to file"""
        try:
            with open(self.user_data_file, 'w', encoding='utf-8') as f:
                json.dump(self.user_data, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving user data: {e}")
    
    def can_generate_fortune(self) -> bool:
        """Check if user can get fortune today"""
        today_str = date.today().isoformat()
        
        for entry in self.user_data["history"]:
            if entry["date"] == today_str:
                return False
        
        return True
    
    def get_todays_fortune(self) -> Optional[Dict]:
        """Get today's fortune if already generated"""
        today_str = date.today().isoformat()
        
        for entry in self.user_data["history"]:
            if entry["date"] == today_str:
                # Find fortune by ID
                for fortune in self.fortunes:
                    if fortune["id"] == entry["fortune_id"]:
                        return {
                            **fortune,
                            "generated_at": entry["timestamp"]
                        }
        
        return None
    
    def generate_fortune(self) -> Dict:
        """Generate new fortune for today"""
        if not self.can_generate_fortune():
            raise ValueError("Fortune already generated for today")
        
        # Get recently used fortune IDs to avoid repeats
        recent_ids = set()
        recent_count = min(len(self.user_data["history"]), 30)  # Last 30 days
        for entry in self.user_data["history"][-recent_count:]:
            recent_ids.add(entry["fortune_id"])
        
        # Filter available fortunes
        available_fortunes = [f for f in self.fortunes if f["id"] not in recent_ids]
        if not available_fortunes:
            available_fortunes = self.fortunes  # Use all if all recent
        
        # Select random fortune
        selected_fortune = random.choice(available_fortunes)
        
        # Record in history
        history_entry = {
            "date": date.today().isoformat(),
            "fortune_id": selected_fortune["id"],
            "timestamp": datetime.now().isoformat()
        }
        
        self.user_data["history"].append(history_entry)
        self._save_user_data()
        
        return {
            **selected_fortune,
            "generated_at": history_entry["timestamp"]
        }
    
    def get_stats(self) -> Dict:
        """Get user statistics"""
        history = self.user_data["history"]
        
        if not history:
            return {
                "total_fortunes": 0,
                "streak": 0,
                "first_fortune": None,
                "last_fortune": None
            }
        
        # Calculate consecutive days streak
        streak = 0
        check_date = date.today()
        
        for entry in reversed(history):
            entry_date = datetime.fromisoformat(entry["date"]).date()
            if entry_date == check_date:
                streak += 1
                check_date = date.fromordinal(check_date.toordinal() - 1)
            else:
                break
        
        return {
            "total_fortunes": len(history),
            "streak": streak,
            "first_fortune": history[0]["date"],
            "last_fortune": history[-1]["date"]
        }