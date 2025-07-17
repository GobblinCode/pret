#!/usr/bin/env python3
"""
Investigation script for themoneyfactory.com to find correct selectors
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from playwright.async_api import async_playwright
from datetime import datetime
from pathlib import Path

async def investigate_themoneyfactory():
    """Investigate the website structure to find correct selectors"""
    
    screenshot_dir = Path("screenshots")
    screenshot_dir.mkdir(exist_ok=True)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Set to False to see what's happening
        
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        )
        
        page = await context.new_page()
        
        try:
            print("🔍 Investigating themoneyfactory.com...")
            
            # Navigate to the main page first
            print("📍 Navigating to main page...")
            await page.goto('https://themoneyfactory.com', wait_until='networkidle', timeout=30000)
            
            # Take screenshot of main page
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            main_screenshot = screenshot_dir / f"main_page_{timestamp}.png"
            await page.screenshot(path=str(main_screenshot), full_page=True)
            print(f"📸 Main page screenshot: {main_screenshot}")
            
            # Check if we can find login links
            print("\n🔍 Looking for login links...")
            login_links = await page.locator('a').all()
            for link in login_links:
                try:
                    text = await link.inner_text()
                    href = await link.get_attribute('href')
                    if any(keyword in text.lower() for keyword in ['login', 'sign in', 'log in', 'account']):
                        print(f"Found login link: '{text}' -> {href}")
                except:
                    pass
            
            # Try to find and click login button/link
            login_selectors = [
                'a[href*="login"]',
                'a:has-text("Login")',
                'a:has-text("Sign in")',
                'a:has-text("Log in")',
                'button:has-text("Login")',
                '.login',
                '#login',
                'a[href*="signin"]',
                'a[href*="account"]'
            ]
            
            login_found = False
            for selector in login_selectors:
                try:
                    element = page.locator(selector).first
                    if await element.is_visible():
                        print(f"✅ Found login element with selector: {selector}")
                        await element.click()
                        await page.wait_for_load_state('networkidle')
                        login_found = True
                        break
                except:
                    continue
            
            if not login_found:
                print("❌ No login link found, trying direct login URL...")
                await page.goto('https://themoneyfactory.com/login', wait_until='networkidle', timeout=30000)
            
            # Take screenshot of login page
            login_screenshot = screenshot_dir / f"login_page_{timestamp}.png"
            await page.screenshot(path=str(login_screenshot), full_page=True)
            print(f"📸 Login page screenshot: {login_screenshot}")
            
            # Investigate form fields
            print("\n🔍 Investigating form fields...")
            
            # Check for input fields
            inputs = await page.locator('input').all()
            print(f"Found {len(inputs)} input fields:")
            
            for i, input_field in enumerate(inputs):
                try:
                    input_type = await input_field.get_attribute('type') or 'text'
                    input_name = await input_field.get_attribute('name') or 'no-name'
                    input_id = await input_field.get_attribute('id') or 'no-id'
                    input_placeholder = await input_field.get_attribute('placeholder') or 'no-placeholder'
                    input_class = await input_field.get_attribute('class') or 'no-class'
                    
                    print(f"  Input {i+1}: type='{input_type}', name='{input_name}', id='{input_id}', placeholder='{input_placeholder}', class='{input_class}'")
                except:
                    print(f"  Input {i+1}: Could not get attributes")
            
            # Check for buttons
            buttons = await page.locator('button').all()
            print(f"\nFound {len(buttons)} buttons:")
            
            for i, button in enumerate(buttons):
                try:
                    button_type = await button.get_attribute('type') or 'button'
                    button_text = await button.inner_text()
                    button_class = await button.get_attribute('class') or 'no-class'
                    
                    print(f"  Button {i+1}: type='{button_type}', text='{button_text}', class='{button_class}'")
                except:
                    print(f"  Button {i+1}: Could not get attributes")
            
            # Get page title and URL
            title = await page.title()
            url = page.url
            print(f"\n📄 Page title: {title}")
            print(f"🌐 Current URL: {url}")
            
            # Check if this is actually a login page
            page_content = await page.content()
            if any(keyword in page_content.lower() for keyword in ['login', 'sign in', 'password', 'email']):
                print("✅ This appears to be a login page")
            else:
                print("❌ This doesn't appear to be a login page")
            
            # Try alternative URLs
            alternative_urls = [
                'https://themoneyfactory.com/signin',
                'https://themoneyfactory.com/account',
                'https://themoneyfactory.com/member',
                'https://themoneyfactory.com/auth/login',
                'https://themoneyfactory.com/user/login'
            ]
            
            for alt_url in alternative_urls:
                try:
                    print(f"\n🔍 Trying alternative URL: {alt_url}")
                    await page.goto(alt_url, wait_until='networkidle', timeout=10000)
                    
                    # Check if we found a login form
                    email_inputs = await page.locator('input[type="email"], input[name*="email"], input[placeholder*="email" i]').count()
                    password_inputs = await page.locator('input[type="password"], input[name*="password"], input[placeholder*="password" i]').count()
                    
                    if email_inputs > 0 and password_inputs > 0:
                        print(f"✅ Found login form at {alt_url}")
                        alt_screenshot = screenshot_dir / f"alt_login_{timestamp}.png"
                        await page.screenshot(path=str(alt_screenshot), full_page=True)
                        print(f"📸 Alternative login screenshot: {alt_screenshot}")
                        break
                except:
                    print(f"❌ Could not access {alt_url}")
            
        except Exception as e:
            print(f"❌ Error during investigation: {str(e)}")
            error_screenshot = screenshot_dir / f"error_{timestamp}.png"
            await page.screenshot(path=str(error_screenshot), full_page=True)
            print(f"📸 Error screenshot: {error_screenshot}")
        
        finally:
            await browser.close()

if __name__ == "__main__":
    print("🔍 Investigating themoneyfactory.com website structure")
    print("=" * 60)
    asyncio.run(investigate_themoneyfactory())