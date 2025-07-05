import asyncio
from datetime import datetime
from .models import db, GamblingSite, ClaimLog
from .automation import BonusClaimAutomation

automation = BonusClaimAutomation()

async def claim_all_bonuses():
    """Claim bonuses for all active sites"""
    results = []
    sites = GamblingSite.query.filter_by(is_active=True).all()
    
    for site in sites:
        # Check if already claimed today
        today = datetime.utcnow().date()
        already_claimed = ClaimLog.query.filter(
            ClaimLog.site_id == site.id,
            db.func.date(ClaimLog.claimed_at) == today,
            ClaimLog.status == 'success'
        ).first()
        
        if already_claimed:
            results.append({
                'site': site.name,
                'status': 'skipped',
                'message': 'Already claimed today'
            })
            continue
        
        # Convert site to dict for automation
        site_config = {
            'name': site.name,
            'url': site.url,
            'login_url': site.login_url,
            'username_selector': site.username_selector,
            'password_selector': site.password_selector,
            'login_button_selector': site.login_button_selector,
            'bonus_claim_selector': site.bonus_claim_selector,
            'username': site.username,
            'password_encrypted': site.password_encrypted,
            'additional_steps': site.additional_steps,
            'cookies': site.cookies
        }
        
        # Run automation
        result = await automation.claim_bonus(site_config)
        
        # Save result to database
        claim_log = ClaimLog(
            site_id=site.id,
            status=result['status'],
            message=result['message'],
            screenshot_path=result['screenshot_path']
        )
        db.session.add(claim_log)
        
        # Update site cookies if successful
        if result['status'] == 'success' and result.get('cookies'):
            site.cookies = result['cookies']
        
        db.session.commit()
        
        results.append({
            'site': site.name,
            'status': result['status'],
            'message': result['message'],
            'screenshot': result['screenshot_path']
        })
    
    return results

def scheduled_claim_task():
    """Wrapper function for scheduler"""
    from . import create_app
    app = create_app()
    
    with app.app_context():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        results = loop.run_until_complete(claim_all_bonuses())
        
        # Log the scheduled run
        print(f"[{datetime.utcnow()}] Daily bonus claim completed:")
        for result in results:
            print(f"  - {result['site']}: {result['status']} - {result['message']}")

def schedule_daily_claims(scheduler):
    """Schedule daily bonus claims"""
    # Schedule for 9 AM UTC daily
    scheduler.add_job(
        id='daily_bonus_claim',
        func=scheduled_claim_task,
        trigger='cron',
        hour=9,
        minute=0,
        replace_existing=True
    )