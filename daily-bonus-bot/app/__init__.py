from flask import Flask
from flask_login import LoginManager
from flask_apscheduler import APScheduler
from .config import Config
from .models import db, User

login_manager = LoginManager()
scheduler = APScheduler()

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    
    # Initialize scheduler
    scheduler.init_app(app)
    scheduler.start()
    
    # Register blueprints
    from .routes import main_bp
    app.register_blueprint(main_bp)
    
    # Create tables
    with app.app_context():
        db.create_all()
        
        # Create default admin user if doesn't exist
        from werkzeug.security import generate_password_hash
        admin = User.query.filter_by(username=app.config['ADMIN_USERNAME']).first()
        if not admin:
            admin = User(
                username=app.config['ADMIN_USERNAME'],
                password_hash=generate_password_hash(app.config['ADMIN_PASSWORD'])
            )
            db.session.add(admin)
            db.session.commit()
    
    # Schedule daily bonus claims
    from .tasks import schedule_daily_claims
    schedule_daily_claims(scheduler)
    
    return app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))