#!/usr/bin/env python3
"""
Investigation script for themoneyfactory.com to find correct selectors
"""

import asyncio
import sys
import os
from pathlib import Path
from playwright.async_api import async_playwright

async def investigate_themoneyfactory():
    """Investigate the structure of themoneyfactory.com"""
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # Run in headless mode
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        page = await context.new_page()
        
        try:
            print("Navigating to themoneyfactory.com...")
            await page.goto('https://themoneyfactory.com', wait_until='networkidle')
            
            # Take a screenshot of the main page
            await page.screenshot(path='screenshots/themoneyfactory_main.png', full_page=True)
            print("Screenshot saved: screenshots/themoneyfactory_main.png")
            
            # Check if there's a login link or button
            print("\nLooking for login elements...")
            
            # Common login link selectors
            login_selectors = [
                'a[href*="login"]',
                'a[href*="sign-in"]',
                'a[href*="signin"]',
                'a:has-text("Login")',
                'a:has-text("Sign In")',
                'a:has-text("Log In")',
                'button:has-text("Login")',
                'button:has-text("Sign In")',
                '.login',
                '#login',
                '.signin',
                '#signin'
            ]
            
            login_found = False
            for selector in login_selectors:
                try:
                    element = await page.wait_for_selector(selector, timeout=2000)
                    if element:
                        href = await element.get_attribute('href')
                        text = await element.inner_text()
                        print(f"Found login element: {selector}")
                        print(f"  Text: {text}")
                        print(f"  Href: {href}")
                        
                        # Click the login link
                        await element.click()
                        await asyncio.sleep(3)
                        login_found = True
                        break
                except:
                    continue
            
            if not login_found:
                print("No login link found, checking if we're already on login page...")
                # Check current URL
                current_url = page.url
                print(f"Current URL: {current_url}")
                
                # Try to navigate to common login URLs
                login_urls = [
                    'https://themoneyfactory.com/login',
                    'https://themoneyfactory.com/signin',
                    'https://themoneyfactory.com/sign-in',
                    'https://themoneyfactory.com/auth/login',
                    'https://themoneyfactory.com/user/login'
                ]
                
                for url in login_urls:
                    try:
                        print(f"Trying to navigate to: {url}")
                        await page.goto(url, wait_until='networkidle')
                        await asyncio.sleep(2)
                        
                        # Check if we found a login form
                        email_selectors = [
                            'input[name="email"]',
                            'input[type="email"]',
                            'input[id="email"]',
                            'input[placeholder*="email" i]',
                            'input[placeholder*="Email" i]',
                            'input[name="username"]',
                            'input[id="username"]',
                            'input[placeholder*="username" i]'
                        ]
                        
                        for selector in email_selectors:
                            try:
                                element = await page.wait_for_selector(selector, timeout=2000)
                                if element:
                                    print(f"Found email/username field: {selector}")
                                    login_found = True
                                    break
                            except:
                                continue
                        
                        if login_found:
                            break
                    except:
                        continue
            
            if login_found:
                print("\nAnalyzing login form...")
                
                # Take screenshot of login page
                await page.screenshot(path='screenshots/themoneyfactory_login.png', full_page=True)
                print("Login page screenshot saved: screenshots/themoneyfactory_login.png")
                
                # Find all input fields
                inputs = await page.query_selector_all('input')
                print(f"\nFound {len(inputs)} input fields:")
                
                for i, input_elem in enumerate(inputs):
                    input_type = await input_elem.get_attribute('type')
                    input_name = await input_elem.get_attribute('name')
                    input_id = await input_elem.get_attribute('id')
                    input_placeholder = await input_elem.get_attribute('placeholder')
                    input_class = await input_elem.get_attribute('class')
                    
                    print(f"  Input {i+1}:")
                    print(f"    Type: {input_type}")
                    print(f"    Name: {input_name}")
                    print(f"    ID: {input_id}")
                    print(f"    Placeholder: {input_placeholder}")
                    print(f"    Class: {input_class}")
                    print()
                
                # Find all buttons
                buttons = await page.query_selector_all('button')
                print(f"Found {len(buttons)} buttons:")
                
                for i, button in enumerate(buttons):
                    button_type = await button.get_attribute('type')
                    button_text = await button.inner_text()
                    button_class = await button.get_attribute('class')
                    button_id = await button.get_attribute('id')
                    
                    print(f"  Button {i+1}:")
                    print(f"    Type: {button_type}")
                    print(f"    Text: {button_text}")
                    print(f"    Class: {button_class}")
                    print(f"    ID: {button_id}")
                    print()
                
                # Find submit inputs
                submit_inputs = await page.query_selector_all('input[type="submit"]')
                print(f"Found {len(submit_inputs)} submit inputs:")
                
                for i, submit in enumerate(submit_inputs):
                    submit_value = await submit.get_attribute('value')
                    submit_class = await submit.get_attribute('class')
                    submit_id = await submit.get_attribute('id')
                    
                    print(f"  Submit {i+1}:")
                    print(f"    Value: {submit_value}")
                    print(f"    Class: {submit_class}")
                    print(f"    ID: {submit_id}")
                    print()
            
            else:
                print("Could not find login form!")
                
                # Get page content for analysis
                content = await page.content()
                print(f"\nPage title: {await page.title()}")
                print(f"Page URL: {page.url}")
                
                # Save page content for manual inspection
                with open('screenshots/themoneyfactory_content.html', 'w') as f:
                    f.write(content)
                print("Page content saved: screenshots/themoneyfactory_content.html")
            
        except Exception as e:
            print(f"Error during investigation: {str(e)}")
            import traceback
            traceback.print_exc()
            
            # Take error screenshot
            await page.screenshot(path='screenshots/themoneyfactory_error.png', full_page=True)
            print("Error screenshot saved: screenshots/themoneyfactory_error.png")
        
        finally:
            await browser.close()

if __name__ == "__main__":
    print("🔍 Investigating themoneyfactory.com structure...")
    print("=" * 50)
    
    # Create screenshots directory
    Path('screenshots').mkdir(exist_ok=True)
    
    asyncio.run(investigate_themoneyfactory())