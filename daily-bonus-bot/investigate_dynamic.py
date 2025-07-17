#!/usr/bin/env python3
"""
Advanced investigation script for themoneyfactory.com that handles dynamic content
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from playwright.async_api import async_playwright
from datetime import datetime
from pathlib import Path

async def investigate_dynamic_content():
    """Investigate the website with dynamic content loading"""
    
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
            print("🔍 Investigating themoneyfactory.com with dynamic content handling...")
            
            # Navigate to the main page first
            print("📍 Navigating to main page...")
            await page.goto('https://themoneyfactory.com', wait_until='networkidle', timeout=30000)
            
            # Wait for potential dynamic content
            print("⏳ Waiting for dynamic content to load...")
            await asyncio.sleep(5)
            
            # Take screenshot of main page
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            main_screenshot = screenshot_dir / f"main_dynamic_{timestamp}.png"
            await page.screenshot(path=str(main_screenshot), full_page=True)
            print(f"📸 Main page screenshot: {main_screenshot}")
            
            # Look for login button and click it
            print("\n🔍 Looking for login button...")
            login_button = page.locator('button:has-text("Login")')
            
            if await login_button.count() > 0:
                print("✅ Found login button, clicking...")
                await login_button.click()
                
                # Wait for login form to appear
                print("⏳ Waiting for login form to load...")
                await asyncio.sleep(3)
                
                # Try to wait for input fields to appear
                try:
                    await page.wait_for_selector('input[type="email"], input[name*="email"], input[placeholder*="email" i]', timeout=10000)
                    print("✅ Email input field appeared!")
                except:
                    print("❌ Email input field did not appear")
                
                # Take screenshot after clicking login
                login_form_screenshot = screenshot_dir / f"login_form_{timestamp}.png"
                await page.screenshot(path=str(login_form_screenshot), full_page=True)
                print(f"📸 Login form screenshot: {login_form_screenshot}")
                
                # Check for input fields again
                print("\n🔍 Checking for input fields after login button click...")
                inputs = await page.locator('input').all()
                print(f"Found {len(inputs)} input fields:")
                
                for i, input_field in enumerate(inputs):
                    try:
                        input_type = await input_field.get_attribute('type') or 'text'
                        input_name = await input_field.get_attribute('name') or 'no-name'
                        input_id = await input_field.get_attribute('id') or 'no-id'
                        input_placeholder = await input_field.get_attribute('placeholder') or 'no-placeholder'
                        input_class = await input_field.get_attribute('class') or 'no-class'
                        is_visible = await input_field.is_visible()
                        
                        print(f"  Input {i+1}: type='{input_type}', name='{input_name}', id='{input_id}', placeholder='{input_placeholder}', visible={is_visible}")
                    except:
                        print(f"  Input {i+1}: Could not get attributes")
                
                # Look for modal or popup
                print("\n🔍 Checking for modal/popup elements...")
                modals = await page.locator('[role="dialog"], .modal, .popup, .MuiDialog-root, .MuiModal-root').all()
                print(f"Found {len(modals)} modal/popup elements")
                
                for i, modal in enumerate(modals):
                    try:
                        is_visible = await modal.is_visible()
                        modal_class = await modal.get_attribute('class') or 'no-class'
                        print(f"  Modal {i+1}: visible={is_visible}, class='{modal_class}'")
                        
                        if is_visible:
                            # Look for inputs inside this modal
                            modal_inputs = await modal.locator('input').all()
                            print(f"    Found {len(modal_inputs)} inputs in this modal")
                            
                            for j, modal_input in enumerate(modal_inputs):
                                try:
                                    input_type = await modal_input.get_attribute('type') or 'text'
                                    input_name = await modal_input.get_attribute('name') or 'no-name'
                                    input_placeholder = await modal_input.get_attribute('placeholder') or 'no-placeholder'
                                    print(f"      Modal Input {j+1}: type='{input_type}', name='{input_name}', placeholder='{input_placeholder}'")
                                except:
                                    pass
                    except:
                        print(f"  Modal {i+1}: Could not get attributes")
                
                # Check for iframes
                print("\n🔍 Checking for iframes...")
                iframes = await page.locator('iframe').all()
                print(f"Found {len(iframes)} iframes")
                
                for i, iframe in enumerate(iframes):
                    try:
                        iframe_src = await iframe.get_attribute('src') or 'no-src'
                        iframe_name = await iframe.get_attribute('name') or 'no-name'
                        print(f"  Iframe {i+1}: src='{iframe_src}', name='{iframe_name}'")
                    except:
                        print(f"  Iframe {i+1}: Could not get attributes")
                
                # Try to find any form elements
                print("\n🔍 Looking for form elements...")
                forms = await page.locator('form').all()
                print(f"Found {len(forms)} forms")
                
                for i, form in enumerate(forms):
                    try:
                        form_action = await form.get_attribute('action') or 'no-action'
                        form_method = await form.get_attribute('method') or 'no-method'
                        is_visible = await form.is_visible()
                        print(f"  Form {i+1}: action='{form_action}', method='{form_method}', visible={is_visible}")
                        
                        if is_visible:
                            form_inputs = await form.locator('input').all()
                            print(f"    Found {len(form_inputs)} inputs in this form")
                    except:
                        print(f"  Form {i+1}: Could not get attributes")
                
                # Wait longer and check again
                print("\n⏳ Waiting longer for dynamic content...")
                await asyncio.sleep(5)
                
                # Final screenshot
                final_screenshot = screenshot_dir / f"final_state_{timestamp}.png"
                await page.screenshot(path=str(final_screenshot), full_page=True)
                print(f"📸 Final state screenshot: {final_screenshot}")
                
            else:
                print("❌ No login button found")
            
        except Exception as e:
            print(f"❌ Error during investigation: {str(e)}")
            import traceback
            traceback.print_exc()
            
            error_screenshot = screenshot_dir / f"error_dynamic_{timestamp}.png"
            await page.screenshot(path=str(error_screenshot), full_page=True)
            print(f"📸 Error screenshot: {error_screenshot}")
        
        finally:
            await browser.close()

if __name__ == "__main__":
    print("🔍 Advanced investigation of themoneyfactory.com with dynamic content")
    print("=" * 70)
    asyncio.run(investigate_dynamic_content())