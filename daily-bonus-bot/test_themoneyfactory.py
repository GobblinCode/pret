#!/usr/bin/env python3
"""
Test script for themoneyfactory.com bot automation
"""

import asyncio
import sys
import os
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.automation import BonusClaimAutomation
from cryptography.fernet import Fernet

async def test_themoneyfactory():
    """Test the bot with themoneyfactory.com"""
    
    # Create automation instance
    automation = BonusClaimAutomation()
    
    # Test credentials
    username = "goblinnationcod@gmail.com"
    password = "Winecooler7!"
    
    # Encrypt password
    encrypted_password = automation.encrypt_password(password)
    
    # Site configuration for themoneyfactory.com
    site_config = {
        'name': 'The Money Factory',
        'url': 'https://themoneyfactory.com',
        'login_url': 'https://themoneyfactory.com',
        'username': username,
        'password_encrypted': encrypted_password,
        'username_selector': 'input[name="email"]',
        'password_selector': 'input[name="password"]',
        'login_button_selector': 'button[type="submit"]:has-text("Login")',
        'bonus_claim_selector': 'button:has-text("Claim"), button:has-text("Bonus"), .bonus-claim, #bonus-claim, .claim-button, button:has-text("Daily")',
        'additional_steps': json.dumps([
            {
                'action': 'click',
                'selector': 'button:has-text("Login")',
                'wait': 2
            }
        ]),
        'cookies': None
    }
    
    print(f"Testing login to {site_config['url']}...")
    print(f"Username: {username}")
    print(f"Password: {'*' * len(password)}")
    print()
    
    try:
        # Test the automation
        result = await automation.claim_bonus(site_config)
        
        print("=== RESULT ===")
        print(f"Status: {result['status']}")
        print(f"Message: {result['message']}")
        print(f"Screenshot: {result['screenshot_path']}")
        
        if result['status'] == 'success':
            print("✅ Bot test successful!")
            if result.get('cookies'):
                print("🍪 Cookies saved for future use")
        else:
            print("❌ Bot test failed!")
            print("This could be due to:")
            print("- Incorrect login credentials")
            print("- Website structure changes")
            print("- Captcha or anti-bot measures")
            print("- Network issues")
            
    except Exception as e:
        print(f"❌ Error during test: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🤖 Testing Daily Bonus Bot with themoneyfactory.com")
    print("=" * 50)
    asyncio.run(test_themoneyfactory())