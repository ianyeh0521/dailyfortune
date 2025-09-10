#!/usr/bin/env python3
"""
Test script for fortune data functionality (no GUI)
"""

from fortune_data import FortuneManager

def main():
    print("🔮 Daily Fortune App - Data Test")
    print("=" * 40)
    
    # Initialize fortune manager
    fm = FortuneManager()
    
    # Show stats
    stats = fm.get_stats()
    print(f"📊 Statistics:")
    print(f"   Total fortunes: {stats['total_fortunes']}")
    print(f"   Current streak: {stats['streak']}")
    print(f"   Device ID: {fm.user_data['device_id']}")
    print()
    
    # Check if can generate fortune
    can_generate = fm.can_generate_fortune()
    print(f"🎯 Can generate today: {can_generate}")
    
    # Get existing fortune or generate new one
    existing_fortune = fm.get_todays_fortune()
    
    if existing_fortune:
        print(f"📜 Today's fortune (already generated):")
        print(f'   "{existing_fortune["text"]}"')
        print(f"   Category: {existing_fortune['category']}")
    elif can_generate:
        print("🎲 Generating new fortune...")
        try:
            new_fortune = fm.generate_fortune()
            print(f"✨ Your fortune:")
            print(f'   "{new_fortune["text"]}"')
            print(f"   Category: {new_fortune['category']}")
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        print("⏰ You've already received today's fortune!")
    
    print()
    print(f"📁 Data stored in: {fm.user_data_file}")
    print(f"📚 Fortune count: {len(fm.fortunes)}")

if __name__ == "__main__":
    main()