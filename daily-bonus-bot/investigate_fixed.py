#!/usr/bin/env python3
"""
Fixed investigation script for themoneyfactory.com that handles multiple login buttons
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from playwright.async_api import async_playwright
from datetime import datetime
from pathlib import Path

async def investigate_fixed():
    """Investigate the website with proper handling of multiple login buttons"""
    
    screenshot_dir = Path("screenshots")
    screenshot_dir.mkdir(exist_ok=True)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        )
        
        page = await context.new_page()
        
        try:
            print("🔍 Investigating themoneyfactory.com with fixed login handling...")
            
            # Navigate to the main page first
            print("📍 Navigating to main page...")
            await page.goto('https://themoneyfactory.com', wait_until='networkidle', timeout=30000)
            
            # Wait for potential dynamic content
            print("⏳ Waiting for dynamic content to load...")
            await asyncio.sleep(5)
            
            # Take screenshot of main page
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            main_screenshot = screenshot_dir / f"main_fixed_{timestamp}.png"
            await page.screenshot(path=str(main_screenshot), full_page=True)
            print(f"📸 Main page screenshot: {main_screenshot}")
            
            # Try different login button selectors
            login_selectors = [
                'button[data-tracking="Home.Header.Login.Btn"]',
                'button[aria-label="Login"]',
                'button:has-text("Login")'
            ]
            
            login_clicked = False
            for selector in login_selectors:
                try:
                    print(f"\n🔍 Trying login selector: {selector}")
                    login_button = page.locator(selector).first
                    
                    if await login_button.count() > 0:
                        print(f"✅ Found login button with selector: {selector}")
                        await login_button.click()
                        login_clicked = True
                        break
                except Exception as e:
                    print(f"❌ Failed with selector {selector}: {str(e)}")
                    continue
            
            if login_clicked:
                print("✅ Successfully clicked login button!")
                
                # Wait for login form to appear
                print("⏳ Waiting for login form to load...")
                await asyncio.sleep(5)
                
                # Take screenshot after clicking login
                login_form_screenshot = screenshot_dir / f"login_form_fixed_{timestamp}.png"
                await page.screenshot(path=str(login_form_screenshot), full_page=True)
                print(f"📸 Login form screenshot: {login_form_screenshot}")
                
                # Look for modal or popup elements that might contain the login form
                print("\n🔍 Checking for modal/popup elements...")
                modal_selectors = [
                    '[role="dialog"]',
                    '.modal',
                    '.popup',
                    '.MuiDialog-root',
                    '.MuiModal-root',
                    '.MuiPaper-root',
                    '[data-testid*="modal"]',
                    '[data-testid*="dialog"]'
                ]
                
                for modal_selector in modal_selectors:
                    try:
                        modals = await page.locator(modal_selector).all()
                        print(f"Found {len(modals)} elements with selector: {modal_selector}")
                        
                        for i, modal in enumerate(modals):
                            try:
                                is_visible = await modal.is_visible()
                                if is_visible:
                                    print(f"  ✅ Modal {i+1} is visible!")
                                    
                                    # Look for inputs inside this modal
                                    modal_inputs = await modal.locator('input').all()
                                    print(f"    Found {len(modal_inputs)} inputs in this modal")
                                    
                                    for j, modal_input in enumerate(modal_inputs):
                                        try:
                                            input_type = await modal_input.get_attribute('type') or 'text'
                                            input_name = await modal_input.get_attribute('name') or 'no-name'
                                            input_placeholder = await modal_input.get_attribute('placeholder') or 'no-placeholder'
                                            input_id = await modal_input.get_attribute('id') or 'no-id'
                                            print(f"      Input {j+1}: type='{input_type}', name='{input_name}', id='{input_id}', placeholder='{input_placeholder}'")
                                        except:
                                            pass
                                    
                                    # Look for buttons inside this modal
                                    modal_buttons = await modal.locator('button').all()
                                    print(f"    Found {len(modal_buttons)} buttons in this modal")
                                    
                                    for j, modal_button in enumerate(modal_buttons):
                                        try:
                                            button_text = await modal_button.inner_text()
                                            button_type = await modal_button.get_attribute('type') or 'button'
                                            print(f"      Button {j+1}: text='{button_text}', type='{button_type}'")
                                        except:
                                            pass
                            except:
                                pass
                    except:
                        pass
                
                # Also check for any visible inputs on the page
                print("\n🔍 Checking for all visible inputs on the page...")
                all_inputs = await page.locator('input').all()
                print(f"Found {len(all_inputs)} total input fields")
                
                visible_inputs = []
                for i, input_field in enumerate(all_inputs):
                    try:
                        is_visible = await input_field.is_visible()
                        if is_visible:
                            input_type = await input_field.get_attribute('type') or 'text'
                            input_name = await input_field.get_attribute('name') or 'no-name'
                            input_placeholder = await input_field.get_attribute('placeholder') or 'no-placeholder'
                            input_id = await input_field.get_attribute('id') or 'no-id'
                            visible_inputs.append({
                                'index': i+1,
                                'type': input_type,
                                'name': input_name,
                                'id': input_id,
                                'placeholder': input_placeholder
                            })
                    except:
                        pass
                
                print(f"Found {len(visible_inputs)} visible inputs:")
                for inp in visible_inputs:
                    print(f"  Input {inp['index']}: type='{inp['type']}', name='{inp['name']}', id='{inp['id']}', placeholder='{inp['placeholder']}'")
                
                # If we found visible inputs, try to test login
                if visible_inputs:
                    print("\n🔍 Attempting to test login with visible inputs...")
                    
                    # Find email and password fields
                    email_field = None
                    password_field = None
                    
                    for inp in visible_inputs:
                        if inp['type'] == 'email' or 'email' in inp['name'].lower() or 'email' in inp['placeholder'].lower():
                            email_field = inp
                        elif inp['type'] == 'password' or 'password' in inp['name'].lower() or 'password' in inp['placeholder'].lower():
                            password_field = inp
                    
                    if email_field and password_field:
                        print(f"✅ Found email field: {email_field}")
                        print(f"✅ Found password field: {password_field}")
                        
                        # Try to fill the form
                        try:
                            # Build selectors
                            email_selector = f"input[type='{email_field['type']}']"
                            if email_field['name'] != 'no-name':
                                email_selector = f"input[name='{email_field['name']}']"
                            elif email_field['id'] != 'no-id':
                                email_selector = f"input[id='{email_field['id']}']"
                            
                            password_selector = f"input[type='{password_field['type']}']"
                            if password_field['name'] != 'no-name':
                                password_selector = f"input[name='{password_field['name']}']"
                            elif password_field['id'] != 'no-id':
                                password_selector = f"input[id='{password_field['id']}']"
                            
                            print(f"Email selector: {email_selector}")
                            print(f"Password selector: {password_selector}")
                            
                            # Fill the form
                            await page.fill(email_selector, "goblinnationcod@gmail.com")
                            await page.fill(password_selector, "Winecooler7!")
                            
                            print("✅ Successfully filled login form!")
                            
                            # Take screenshot after filling
                            filled_screenshot = screenshot_dir / f"form_filled_{timestamp}.png"
                            await page.screenshot(path=str(filled_screenshot), full_page=True)
                            print(f"📸 Form filled screenshot: {filled_screenshot}")
                            
                            # Look for submit button
                            submit_selectors = [
                                'button[type="submit"]',
                                'input[type="submit"]',
                                'button:has-text("Login")',
                                'button:has-text("Sign in")',
                                'button:has-text("Log in")',
                                'button:has-text("Submit")'
                            ]
                            
                            for submit_selector in submit_selectors:
                                try:
                                    submit_button = page.locator(submit_selector).first
                                    if await submit_button.count() > 0 and await submit_button.is_visible():
                                        print(f"✅ Found submit button: {submit_selector}")
                                        await submit_button.click()
                                        print("✅ Clicked submit button!")
                                        
                                        # Wait for response
                                        await asyncio.sleep(3)
                                        
                                        # Take final screenshot
                                        final_screenshot = screenshot_dir / f"login_attempt_{timestamp}.png"
                                        await page.screenshot(path=str(final_screenshot), full_page=True)
                                        print(f"📸 Login attempt screenshot: {final_screenshot}")
                                        
                                        # Check current URL
                                        current_url = page.url
                                        print(f"Current URL after login attempt: {current_url}")
                                        
                                        break
                                except:
                                    continue
                            
                        except Exception as e:
                            print(f"❌ Error filling form: {str(e)}")
                    else:
                        print("❌ Could not find both email and password fields")
                else:
                    print("❌ No visible inputs found")
                
            else:
                print("❌ Could not click any login button")
            
        except Exception as e:
            print(f"❌ Error during investigation: {str(e)}")
            import traceback
            traceback.print_exc()
            
            error_screenshot = screenshot_dir / f"error_fixed_{timestamp}.png"
            await page.screenshot(path=str(error_screenshot), full_page=True)
            print(f"📸 Error screenshot: {error_screenshot}")
        
        finally:
            await browser.close()

if __name__ == "__main__":
    print("🔍 Fixed investigation of themoneyfactory.com")
    print("=" * 50)
    asyncio.run(investigate_fixed())