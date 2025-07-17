#!/usr/bin/env python3
"""
Fixed test script for themoneyfactory.com bot automation
"""

import asyncio
import sys
import os
import json
from pathlib import Path
from playwright.async_api import async_playwright
from datetime import datetime

async def test_themoneyfactory_login():
    """Test login and investigate post-login state"""
    
    username = "goblinnationcod@gmail.com"
    password = "Winecooler7!"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        page = await context.new_page()
        
        try:
            print("1. Navigating to themoneyfactory.com...")
            await page.goto('https://themoneyfactory.com', wait_until='networkidle')
            
            # Take screenshot of main page
            await page.screenshot(path='screenshots/step1_main.png', full_page=True)
            print("   Screenshot saved: screenshots/step1_main.png")
            
            print("2. Clicking login button to open modal...")
            await page.click('button:has-text("Login")')
            await asyncio.sleep(2)
            
            # Take screenshot after clicking login
            await page.screenshot(path='screenshots/step2_login_modal.png', full_page=True)
            print("   Screenshot saved: screenshots/step2_login_modal.png")
            
            print("3. Filling login form...")
            await page.fill('input[name="email"]', username)
            await page.fill('input[name="password"]', password)
            
            # Take screenshot after filling form
            await page.screenshot(path='screenshots/step3_filled_form.png', full_page=True)
            print("   Screenshot saved: screenshots/step3_filled_form.png")
            
            print("4. Submitting login form...")
            await page.click('button[type="submit"]:has-text("Login")')
            await asyncio.sleep(5)  # Wait for login to complete
            
            # Take screenshot after login
            await page.screenshot(path='screenshots/step4_after_login.png', full_page=True)
            print("   Screenshot saved: screenshots/step4_after_login.png")
            
            print("5. Checking current URL and page state...")
            current_url = page.url
            print(f"   Current URL: {current_url}")
            
            # Check if we're logged in by looking for user-specific elements
            try:
                # Look for common post-login elements
                user_elements = await page.query_selector_all('button:has-text("Profile"), button:has-text("Account"), button:has-text("Logout"), .user-menu, .profile')
                print(f"   Found {len(user_elements)} user-related elements")
                
                # Check for bonus-related elements
                bonus_elements = await page.query_selector_all('button:has-text("Claim"), button:has-text("Bonus"), button:has-text("Daily"), .bonus, .claim')
                print(f"   Found {len(bonus_elements)} bonus-related elements")
                
                if bonus_elements:
                    print("   Bonus elements found:")
                    for i, elem in enumerate(bonus_elements[:5]):  # Show first 5
                        try:
                            text = await elem.inner_text()
                            classes = await elem.get_attribute('class')
                            print(f"     {i+1}. Text: '{text}' | Classes: {classes}")
                        except:
                            print(f"     {i+1}. Could not get element info")
                
            except Exception as e:
                print(f"   Error checking elements: {e}")
            
            print("6. Looking for daily bonus or claim buttons...")
            
            # Try different approaches to find bonus claim buttons
            bonus_selectors = [
                'button:has-text("Daily")',
                'button:has-text("Claim")',
                'button:has-text("Bonus")',
                'button[data-testid*="claim"]',
                'button[data-testid*="bonus"]',
                'button[data-testid*="daily"]',
                '.daily-bonus',
                '.claim-bonus',
                '.bonus-claim'
            ]
            
            for selector in bonus_selectors:
                try:
                    elements = await page.query_selector_all(selector)
                    if elements:
                        print(f"   Found {len(elements)} elements with selector: {selector}")
                        for i, elem in enumerate(elements[:3]):  # Show first 3
                            try:
                                text = await elem.inner_text()
                                visible = await elem.is_visible()
                                enabled = await elem.is_enabled()
                                print(f"     {i+1}. Text: '{text}' | Visible: {visible} | Enabled: {enabled}")
                            except:
                                print(f"     {i+1}. Could not get element info")
                except:
                    continue
            
            print("7. Checking for navigation menu or dashboard...")
            
            # Look for navigation or menu items
            nav_selectors = [
                'nav a',
                '.nav-link',
                '.menu-item',
                'button:has-text("Dashboard")',
                'button:has-text("Games")',
                'button:has-text("Promotions")',
                'a:has-text("Promotions")',
                'a:has-text("Bonuses")'
            ]
            
            for selector in nav_selectors:
                try:
                    elements = await page.query_selector_all(selector)
                    if elements:
                        print(f"   Found {len(elements)} navigation elements with selector: {selector}")
                        for i, elem in enumerate(elements[:3]):  # Show first 3
                            try:
                                text = await elem.inner_text()
                                href = await elem.get_attribute('href')
                                print(f"     {i+1}. Text: '{text}' | Href: {href}")
                            except:
                                print(f"     {i+1}. Could not get element info")
                except:
                    continue
            
            print("8. Trying to close any open modals...")
            
            # Try to close modals
            modal_close_selectors = [
                '.modal-close',
                '.close',
                'button[aria-label="close"]',
                'button[aria-label="Close"]',
                '.MuiDialog-root button',
                '.modal-close-btn'
            ]
            
            for selector in modal_close_selectors:
                try:
                    elements = await page.query_selector_all(selector)
                    if elements:
                        print(f"   Found {len(elements)} modal close elements with selector: {selector}")
                        for elem in elements:
                            try:
                                visible = await elem.is_visible()
                                if visible:
                                    await elem.click()
                                    await asyncio.sleep(1)
                                    print(f"     Clicked close button")
                                    break
                            except:
                                continue
                except:
                    continue
            
            # Take final screenshot
            await page.screenshot(path='screenshots/step8_final_state.png', full_page=True)
            print("   Final screenshot saved: screenshots/step8_final_state.png")
            
            print("9. Final analysis complete!")
            
        except Exception as e:
            print(f"❌ Error during test: {str(e)}")
            import traceback
            traceback.print_exc()
            
            # Take error screenshot
            await page.screenshot(path='screenshots/error_state.png', full_page=True)
            print("Error screenshot saved: screenshots/error_state.png")
        
        finally:
            await browser.close()

if __name__ == "__main__":
    print("🔍 Testing themoneyfactory.com login and post-login state...")
    print("=" * 60)
    
    # Create screenshots directory
    Path('screenshots').mkdir(exist_ok=True)
    
    asyncio.run(test_themoneyfactory_login())