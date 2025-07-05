from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from .models import db, User, GamblingSite, ClaimLog
from .automation import BonusClaimAutomation
import asyncio
import json
from datetime import datetime, timedelta

main_bp = Blueprint('main', __name__)
automation = BonusClaimAutomation()

@main_bp.route('/')
@login_required
def index():
    sites = GamblingSite.query.all()
    recent_claims = ClaimLog.query.order_by(ClaimLog.claimed_at.desc()).limit(10).all()
    
    # Calculate success rate for each site
    for site in sites:
        total_claims = len(site.claims)
        successful_claims = sum(1 for claim in site.claims if claim.status == 'success')
        site.success_rate = (successful_claims / total_claims * 100) if total_claims > 0 else 0
        
        # Check if claimed today
        today = datetime.utcnow().date()
        site.claimed_today = any(
            claim.claimed_at.date() == today and claim.status == 'success' 
            for claim in site.claims
        )
    
    return render_template('index.html', sites=sites, recent_claims=recent_claims)

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user, remember=True)
            return redirect(url_for('main.index'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main_bp.route('/sites')
@login_required
def sites():
    sites = GamblingSite.query.all()
    return render_template('sites.html', sites=sites)

@main_bp.route('/sites/add', methods=['GET', 'POST'])
@login_required
def add_site():
    if request.method == 'POST':
        site = GamblingSite(
            name=request.form.get('name'),
            url=request.form.get('url'),
            login_url=request.form.get('login_url'),
            username_selector=request.form.get('username_selector'),
            password_selector=request.form.get('password_selector'),
            login_button_selector=request.form.get('login_button_selector'),
            bonus_claim_selector=request.form.get('bonus_claim_selector'),
            username=request.form.get('username'),
            is_active=request.form.get('is_active') == 'on'
        )
        
        # Encrypt password
        password = request.form.get('password')
        if password:
            site.password_encrypted = automation.encrypt_password(password)
        
        # Handle additional steps
        additional_steps = request.form.get('additional_steps')
        if additional_steps:
            try:
                json.loads(additional_steps)  # Validate JSON
                site.additional_steps = additional_steps
            except:
                flash('Invalid JSON format for additional steps', 'error')
                return render_template('add_site.html')
        
        db.session.add(site)
        db.session.commit()
        
        flash('Site added successfully', 'success')
        return redirect(url_for('main.sites'))
    
    return render_template('add_site.html')

@main_bp.route('/sites/<int:site_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_site(site_id):
    site = GamblingSite.query.get_or_404(site_id)
    
    if request.method == 'POST':
        site.name = request.form.get('name')
        site.url = request.form.get('url')
        site.login_url = request.form.get('login_url')
        site.username_selector = request.form.get('username_selector')
        site.password_selector = request.form.get('password_selector')
        site.login_button_selector = request.form.get('login_button_selector')
        site.bonus_claim_selector = request.form.get('bonus_claim_selector')
        site.username = request.form.get('username')
        site.is_active = request.form.get('is_active') == 'on'
        
        # Update password if provided
        password = request.form.get('password')
        if password:
            site.password_encrypted = automation.encrypt_password(password)
        
        # Handle additional steps
        additional_steps = request.form.get('additional_steps')
        if additional_steps:
            try:
                json.loads(additional_steps)  # Validate JSON
                site.additional_steps = additional_steps
            except:
                flash('Invalid JSON format for additional steps', 'error')
                return render_template('edit_site.html', site=site)
        
        # Handle cookies
        cookies = request.form.get('cookies')
        if cookies:
            try:
                json.loads(cookies)  # Validate JSON
                site.cookies = cookies
            except:
                flash('Invalid JSON format for cookies', 'error')
                return render_template('edit_site.html', site=site)
        
        site.updated_at = datetime.utcnow()
        db.session.commit()
        
        flash('Site updated successfully', 'success')
        return redirect(url_for('main.sites'))
    
    return render_template('edit_site.html', site=site)

@main_bp.route('/sites/<int:site_id>/delete', methods=['POST'])
@login_required
def delete_site(site_id):
    site = GamblingSite.query.get_or_404(site_id)
    db.session.delete(site)
    db.session.commit()
    
    flash('Site deleted successfully', 'success')
    return redirect(url_for('main.sites'))

@main_bp.route('/sites/<int:site_id>/test', methods=['POST'])
@login_required
def test_site(site_id):
    site = GamblingSite.query.get_or_404(site_id)
    
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
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(automation.claim_bonus(site_config))
    
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
    
    return jsonify(result)

@main_bp.route('/claims')
@login_required
def claims():
    page = request.args.get('page', 1, type=int)
    claims = ClaimLog.query.order_by(ClaimLog.claimed_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template('claims.html', claims=claims)

@main_bp.route('/api/claim-all', methods=['POST'])
@login_required
def claim_all():
    """Manually trigger claiming bonuses for all active sites"""
    from .tasks import claim_all_bonuses
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    results = loop.run_until_complete(claim_all_bonuses())
    
    return jsonify({
        'status': 'completed',
        'results': results
    })