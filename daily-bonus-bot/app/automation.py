import asyncio
import json
import os
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright
from cryptography.fernet import Fernet
import base64

class BonusClaimAutomation:
    def __init__(self, screenshot_dir="screenshots"):
        self.screenshot_dir = Path(screenshot_dir)
        self.screenshot_dir.mkdir(exist_ok=True)
        # Generate a key for encryption (in production, store this securely)
        self.cipher_key = os.environ.get('CIPHER_KEY') or Fernet.generate_key()
        self.cipher = Fernet(self.cipher_key)
    
    def encrypt_password(self, password):
        """Encrypt password for storage"""
        return self.cipher.encrypt(password.encode()).decode()
    
    def decrypt_password(self, encrypted_password):
        """Decrypt password for use"""
        return self.cipher.decrypt(encrypted_password.encode()).decode()
    
    async def claim_bonus(self, site_config):
        """Main function to claim bonus from a gambling site"""
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=['--disable-blink-features=AutomationControlled']
            )
            
            context = await browser.new_context(
                viewport={'width': 390, 'height': 844},  # iPhone 12 Pro viewport
                user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1'
            )
            
            # Load cookies if available
            if site_config.get('cookies'):
                await context.add_cookies(json.loads(site_config['cookies']))
            
            page = await context.new_page()
            result = {
                'status': 'failed',
                'message': '',
                'screenshot_path': None,
                'bonus_amount': None
            }
            
            try:
                # Navigate to login page
                login_url = site_config.get('login_url') or site_config['url']
                await page.goto(login_url, wait_until='networkidle')
                
                # Check if already logged in by looking for bonus claim element
                if site_config.get('bonus_claim_selector'):
                    try:
                        await page.wait_for_selector(site_config['bonus_claim_selector'], timeout=5000)
                        # Already logged in, proceed to claim
                    except:
                        # Need to login
                        await self._perform_login(page, site_config)
                else:
                    # Always perform login if no bonus selector provided
                    await self._perform_login(page, site_config)
                
                # Execute additional navigation steps if provided
                if site_config.get('additional_steps'):
                    steps = json.loads(site_config['additional_steps'])
                    await self._execute_steps(page, steps)
                
                # Claim the bonus
                if site_config.get('bonus_claim_selector'):
                    await page.wait_for_selector(site_config['bonus_claim_selector'], timeout=10000)
                    await page.click(site_config['bonus_claim_selector'])
                    await asyncio.sleep(2)  # Wait for action to complete
                
                # Take screenshot
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                screenshot_name = f"{site_config['name'].replace(' ', '_')}_{timestamp}.png"
                screenshot_path = self.screenshot_dir / screenshot_name
                await page.screenshot(path=str(screenshot_path), full_page=True)
                
                # Save cookies for future use
                cookies = await context.cookies()
                
                result = {
                    'status': 'success',
                    'message': 'Bonus claimed successfully',
                    'screenshot_path': str(screenshot_path),
                    'cookies': json.dumps(cookies)
                }
                
            except Exception as e:
                result['message'] = str(e)
                # Take error screenshot
                try:
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    screenshot_name = f"{site_config['name'].replace(' ', '_')}_error_{timestamp}.png"
                    screenshot_path = self.screenshot_dir / screenshot_name
                    await page.screenshot(path=str(screenshot_path), full_page=True)
                    result['screenshot_path'] = str(screenshot_path)
                except:
                    pass
            
            finally:
                await browser.close()
            
            return result
    
    async def _perform_login(self, page, site_config):
        """Perform login steps"""
        if not all([site_config.get('username'), site_config.get('password_encrypted'),
                   site_config.get('username_selector'), site_config.get('password_selector')]):
            raise Exception("Missing login credentials or selectors")
        
        # Decrypt password
        password = self.decrypt_password(site_config['password_encrypted'])
        
        # Fill login form
        await page.fill(site_config['username_selector'], site_config['username'])
        await page.fill(site_config['password_selector'], password)
        
        # Click login button
        if site_config.get('login_button_selector'):
            await page.click(site_config['login_button_selector'])
        else:
            # Try common login button selectors
            for selector in ['button[type="submit"]', 'input[type="submit"]', 'button:has-text("Login")', 'button:has-text("Sign in")']:
                try:
                    await page.click(selector, timeout=2000)
                    break
                except:
                    continue
        
        # Wait for navigation
        await asyncio.sleep(3)
    
    async def _execute_steps(self, page, steps):
        """Execute additional navigation steps"""
        for step in steps:
            action = step.get('action')
            
            if action == 'click':
                await page.click(step['selector'])
                await asyncio.sleep(step.get('wait', 1))
            
            elif action == 'fill':
                await page.fill(step['selector'], step['value'])
                await asyncio.sleep(step.get('wait', 0.5))
            
            elif action == 'navigate':
                await page.goto(step['url'], wait_until='networkidle')
                await asyncio.sleep(step.get('wait', 1))
            
            elif action == 'wait':
                await asyncio.sleep(step.get('seconds', 1))
            
            elif action == 'wait_for_selector':
                await page.wait_for_selector(step['selector'], timeout=step.get('timeout', 10000))