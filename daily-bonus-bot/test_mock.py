#!/usr/bin/env python3
import asyncio
from app.automation_mock import BonusClaimAutomation

async def test_mock():
    automation = BonusClaimAutomation()
    
    # Test site configuration
    site_config = {
        'name': 'Test Casino',
        'url': 'https://example.com',
        'username': 'testuser',
        'password_encrypted': automation.encrypt_password('testpass')
    }
    
    print("Testing mock automation...")
    result = await automation.claim_bonus(site_config)
    
    print(f"Status: {result['status']}")
    print(f"Message: {result['message']}")
    print(f"Screenshot: {result['screenshot_path']}")
    if result.get('bonus_amount'):
        print(f"Bonus Amount: {result['bonus_amount']}")

if __name__ == '__main__':
    asyncio.run(test_mock())