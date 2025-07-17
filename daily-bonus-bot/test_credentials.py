#!/usr/bin/env python3
"""
Test credentials for themoneyfactory.com
"""

import asyncio
import sys
import os
import json
from pathlib import Path
from playwright.async_api import async_playwright
from datetime import datetime

async def test_credentials():
    """Test the credentials and form validation"""
    
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
            
            print("2. Clicking login button to open modal...")
            await page.click('button:has-text("Login")')
            await asyncio.sleep(2)
            
            print("3. Checking form validation...")
            
            # Get the email and password fields
            email_field = await page.query_selector('input[name="email"]')
            password_field = await page.query_selector('input[name="password"]')
            login_button = await page.query_selector('button[type="submit"]:has-text("Login")')
            
            if not email_field or not password_field or not login_button:
                print("   ❌ Could not find form elements")
                return
            
            print("   ✅ Found all form elements")
            
            # Check initial button state
            button_enabled = await login_button.is_enabled()
            print(f"   Initial button enabled: {button_enabled}")
            
            print("4. Filling email field...")
            await email_field.fill(username)
            await asyncio.sleep(1)
            
            # Check button state after email
            button_enabled = await login_button.is_enabled()
            print(f"   Button enabled after email: {button_enabled}")
            
            print("5. Filling password field...")
            await password_field.fill(password)
            await asyncio.sleep(1)
            
            # Check button state after password
            button_enabled = await login_button.is_enabled()
            print(f"   Button enabled after password: {button_enabled}")
            
            # Wait a bit more for validation
            print("6. Waiting for form validation...")
            await asyncio.sleep(2)
            
            button_enabled = await login_button.is_enabled()
            print(f"   Button enabled after wait: {button_enabled}")
            
            # Check for any validation errors
            error_elements = await page.query_selector_all('.error, .invalid, .field-error, [role="alert"]')
            if error_elements:
                print(f"   Found {len(error_elements)} potential error elements:")
                for i, elem in enumerate(error_elements):
                    try:
                        text = await elem.inner_text()
                        if text.strip():
                            print(f"     {i+1}. {text}")
                    except:
                        pass
            
            # Try different approaches to enable the button
            print("7. Trying to trigger validation...")
            
            # Try clicking on the fields to trigger validation
            await email_field.click()
            await asyncio.sleep(0.5)
            await password_field.click()
            await asyncio.sleep(0.5)
            
            # Try pressing Tab to trigger validation
            await password_field.press('Tab')
            await asyncio.sleep(1)
            
            button_enabled = await login_button.is_enabled()
            print(f"   Button enabled after validation triggers: {button_enabled}")
            
            # Check if there are any required fields we missed
            all_inputs = await page.query_selector_all('input')
            print(f"   Found {len(all_inputs)} total input fields:")
            
            for i, input_elem in enumerate(all_inputs):
                try:
                    input_type = await input_elem.get_attribute('type')
                    input_name = await input_elem.get_attribute('name')
                    input_id = await input_elem.get_attribute('id')
                    input_required = await input_elem.get_attribute('required')
                    input_value = await input_elem.input_value()
                    
                    print(f"     {i+1}. Type: {input_type}, Name: {input_name}, ID: {input_id}, Required: {input_required}, Value: {'*' * len(input_value) if input_value else 'empty'}")
                except:
                    print(f"     {i+1}. Could not get input info")
            
            # If button is still disabled, try force clicking
            if not button_enabled:
                print("8. Button still disabled, trying force click...")
                try:
                    await login_button.click(force=True)
                    await asyncio.sleep(3)
                    print("   Force click successful")
                except Exception as e:
                    print(f"   Force click failed: {e}")
            else:
                print("8. Button is enabled, clicking normally...")
                await login_button.click()
                await asyncio.sleep(3)
                print("   Normal click successful")
            
            # Check the result
            current_url = page.url
            print(f"9. Current URL after login attempt: {current_url}")
            
            # Take final screenshot
            await page.screenshot(path='screenshots/credential_test.png', full_page=True)
            print("   Screenshot saved: screenshots/credential_test.png")
            
        except Exception as e:
            print(f"❌ Error during test: {str(e)}")
            import traceback
            traceback.print_exc()
            
            # Take error screenshot
            await page.screenshot(path='screenshots/credential_error.png', full_page=True)
            print("Error screenshot saved: screenshots/credential_error.png")
        
        finally:
            await browser.close()

if __name__ == "__main__":
    print("🔍 Testing credentials and form validation...")
    print("=" * 50)
    
    # Create screenshots directory
    Path('screenshots').mkdir(exist_ok=True)
    
    asyncio.run(test_credentials())