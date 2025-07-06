import asyncio
import json
import os
import random
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
    
    async def human_delay(self, min_seconds=1.0, max_seconds=3.0):
        """Add human-like random delays"""
        delay = random.uniform(min_seconds, max_seconds)
        await asyncio.sleep(delay)
    
    async def human_type(self, page, selector, text):
        """Type text like a human with random delays between characters"""
        await page.click(selector)
        await self.human_delay(0.5, 1)
        
        for char in text:
            await page.type(selector, char, delay=random.uniform(50, 150))
            await asyncio.sleep(random.uniform(0.05, 0.15))
        
        await self.human_delay(0.5, 1.5)
    
    async def human_click(self, page, selector):
        """Click like a human with proper delays"""
        # Move to element first
        element = await page.query_selector(selector)
        if element:
            await element.hover()
            await self.human_delay(0.3, 0.8)
        
        await page.click(selector)
        await self.human_delay(1, 2)
    
    async def wait_for_captcha(self, page, timeout=30):
        """Wait for captcha to complete and handle Cloudflare verification"""
        print("🔄 Waiting for captcha/verification to complete...")
        start_time = datetime.now()
        
        while (datetime.now() - start_time).seconds < timeout:
            # Check for Cloudflare "Verify you are human" checkbox
            cloudflare_selectors = [
                "input[type='checkbox']",
                ".cf-checkbox",
                "#cf-checkbox",
                "[name*='cf']",
                "iframe[src*='cloudflare']",
                "iframe[src*='turnstile']",
                ".cf-turnstile"
            ]
            
            # Try to find and click Cloudflare checkbox
            for selector in cloudflare_selectors:
                try:
                    element = await page.query_selector(selector)
                    if element:
                        print(f"✅ Found Cloudflare element: {selector}")
                        # Try to click the checkbox
                        try:
                            await element.click()
                            print("✅ Clicked Cloudflare checkbox")
                            await self.human_delay(2, 4)
                        except:
                            # If direct click fails, try to find the label and click it
                            try:
                                label = await page.query_selector("label[for*='cf'], label:has-text('Verify you are human')")
                                if label:
                                    await label.click()
                                    print("✅ Clicked Cloudflare label")
                                    await self.human_delay(2, 4)
                            except:
                                pass
                        break
                except:
                    continue
            
            # Check if verification is complete
            verification_selectors = [
                "iframe[src*='captcha']",
                ".captcha",
                "#captcha",
                "[class*='captcha']",
                "[id*='captcha']",
                "iframe[src*='turnstile']",
                ".cf-turnstile",
                "input[type='checkbox']:not(:checked)"
            ]
            
            verification_found = False
            for selector in verification_selectors:
                try:
                    element = await page.query_selector(selector)
                    if element:
                        verification_found = True
                        break
                except:
                    continue
            
            if not verification_found:
                print("✅ Verification appears to be completed")
                return True
            
            await asyncio.sleep(2)
        
        print("⏰ Verification timeout - proceeding anyway")
        return False
    
    async def handle_cloudflare_verification(self, page):
        """Handle Cloudflare verification before login"""
        print("🔍 Checking for Cloudflare verification...")
        
        # Look for Cloudflare verification elements
        cloudflare_selectors = [
            "input[type='checkbox']",
            ".cf-checkbox",
            "#cf-checkbox",
            "[name*='cf']",
            "iframe[src*='cloudflare']",
            "iframe[src*='turnstile']",
            ".cf-turnstile",
            "label:has-text('Verify you are human')",
            "label:has-text('I am human')"
        ]
        
        for selector in cloudflare_selectors:
            try:
                element = await page.query_selector(selector)
                if element:
                    print(f"✅ Found Cloudflare verification: {selector}")
                    
                    # Try to click the element
                    try:
                        await element.click()
                        print("✅ Clicked Cloudflare verification element")
                        await self.human_delay(2, 4)
                        return True
                    except:
                        # If direct click fails, try clicking the label
                        try:
                            label = await page.query_selector("label[for*='cf'], label:has-text('Verify you are human')")
                            if label:
                                await label.click()
                                print("✅ Clicked Cloudflare label")
                                await self.human_delay(2, 4)
                                return True
                        except:
                            pass
            except:
                continue
        
        print("ℹ️ No Cloudflare verification found")
        return False
    
    async def handle_cookie_popup(self, page):
        """Handle cookie acceptance popups"""
        print("🍪 Checking for cookie popup...")
        
        # Common cookie popup selectors
        cookie_selectors = [
            "button:has-text('Accept All')",
            "button:has-text('Accept')",
            "button:has-text('Allow All')",
            "button:has-text('Allow')",
            "button:has-text('OK')",
            "button:has-text('Got it')",
            "button:has-text('I agree')",
            "button:has-text('Accept cookies')",
            "button:has-text('Accept all cookies')",
            ".accept-cookies",
            ".cookie-accept",
            "#accept-cookies",
            "#cookie-accept",
            "[data-testid*='accept']",
            "[data-testid*='cookie']"
        ]
        
        for selector in cookie_selectors:
            try:
                element = await page.query_selector(selector)
                if element:
                    print(f"✅ Found cookie popup: {selector}")
                    await element.click()
                    print("✅ Clicked cookie accept button")
                    await self.human_delay(1, 2)
                    return True
            except:
                continue
        
        print("ℹ️ No cookie popup found")
        return False
    
    def encrypt_password(self, password):
        """Encrypt password for storage"""
        return self.cipher.encrypt(password.encode()).decode()
    
    def decrypt_password(self, encrypted_password):
        """Decrypt password for use"""
        return self.cipher.decrypt(encrypted_password.encode()).decode()
    
    async def claim_bonus(self, site_config):
        """Main function to claim bonus from a gambling site with human-like behavior"""
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=False,  # Set to False for debugging
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor'
                ]
            )
            
            context = await browser.new_context(
                viewport={'width': 1280, 'height': 720},  # Desktop viewport
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
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
                print(f"🌐 Navigating to: {login_url}")
                try:
                    await page.goto(login_url, wait_until='networkidle', timeout=60000)
                except:
                    print("⚠️ Network timeout, trying with domcontentloaded...")
                    await page.goto(login_url, wait_until='domcontentloaded', timeout=60000)
                await self.human_delay(2, 4)
                
                # Handle cookie popup before proceeding
                await self.handle_cookie_popup(page)
                
                # Check if already logged in by looking for bonus claim element
                if site_config.get('bonus_claim_selector'):
                    try:
                        await page.wait_for_selector(site_config['bonus_claim_selector'], timeout=5000)
                        print("✅ Already logged in, proceeding to claim")
                    except:
                        print("🔐 Need to login first")
                        await self._perform_login(page, site_config)
                else:
                    # Always perform login if no bonus selector provided
                    print("🔐 Performing login")
                    await self._perform_login(page, site_config)
                
                # Execute additional navigation steps if provided
                if site_config.get('additional_steps'):
                    steps = json.loads(site_config['additional_steps'])
                    await self._execute_human_steps(page, steps)
                
                # Claim the bonus
                if site_config.get('bonus_claim_selector'):
                    print("🎁 Looking for bonus claim button...")
                    await page.wait_for_selector(site_config['bonus_claim_selector'], timeout=10000)
                    await self.human_click(page, site_config['bonus_claim_selector'])
                    await self.human_delay(2, 4)
                
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
        """Perform login steps with human-like behavior"""
        if not all([site_config.get('username'), site_config.get('password_encrypted'),
                   site_config.get('username_selector'), site_config.get('password_selector')]):
            raise Exception("Missing login credentials or selectors")
        
        # Decrypt password
        password = self.decrypt_password(site_config['password_encrypted'])
        
        print("👤 Filling username...")
        await self.human_type(page, site_config['username_selector'], site_config['username'])
        
        print("🔒 Filling password...")
        await self.human_type(page, site_config['password_selector'], password)
        
        # Check for Cloudflare verification before login
        await self.handle_cloudflare_verification(page)
        
        # Wait a bit before clicking login
        await self.human_delay(1, 3)
        
        # Click login button
        if site_config.get('login_button_selector'):
            print("🔘 Clicking login button...")
            await self.human_click(page, site_config['login_button_selector'])
        else:
            # Try common login button selectors
            login_selectors = ['button[type="submit"]', 'input[type="submit"]', 'button:has-text("Login")', 'button:has-text("Sign in")']
            for selector in login_selectors:
                try:
                    print(f"🔘 Trying login button: {selector}")
                    await self.human_click(page, selector)
                    break
                except:
                    continue
        
        # Wait for captcha to complete
        await self.wait_for_captcha(page)
        
        # Wait for navigation
        await self.human_delay(3, 6)
        
        print("✅ Login process completed")
    
    async def _execute_human_steps(self, page, steps):
        """Execute additional navigation steps with human-like behavior"""
        for i, step in enumerate(steps):
            action = step.get('action')
            print(f"🔄 Step {i+1}: {action}")
            
            if action == 'click':
                await self.human_click(page, step['selector'])
                await self.human_delay(step.get('wait', 1), step.get('wait', 1) + 1)
            
            elif action == 'fill':
                await self.human_type(page, step['selector'], step['value'])
                await self.human_delay(step.get('wait', 0.5), step.get('wait', 0.5) + 0.5)
            
            elif action == 'navigate':
                await page.goto(step['url'], wait_until='networkidle')
                await self.human_delay(step.get('wait', 2), step.get('wait', 2) + 2)
            
            elif action == 'wait':
                await self.human_delay(step.get('seconds', 1), step.get('seconds', 1) + 1)
            
            elif action == 'wait_for_selector':
                await page.wait_for_selector(step['selector'], timeout=step.get('timeout', 10000))
                await self.human_delay(1, 2)
            
            elif action == 'scroll':
                direction = step.get('direction', 'down')
                if direction == 'down':
                    await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                elif direction == 'up':
                    await page.evaluate("window.scrollTo(0, 0)")
                await self.human_delay(step.get('wait', 2), step.get('wait', 2) + 1)
    
    async def _execute_steps(self, page, steps):
        """Execute additional navigation steps (legacy method)"""
        await self._execute_human_steps(page, steps)