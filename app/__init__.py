from flask import Flask
from flask_login import LoginManager
from app.models.models import db, User
from config import Config

# Initialize Flask app
app = Flask(__name__, static_url_path='/static')
app.config.from_object(Config)

# Initialize SQLAlchemy
db.init_app(app)

# Initialize LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Import and register Blueprints
def register_blueprints(app):
    from app.routes.auth import auth_bp
    from app.routes.transactions import transactions_bp
    from app.routes.dashboard import dashboard_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(transactions_bp)
    app.register_blueprint(dashboard_bp)

register_blueprints(app)

def create_app():
    return app
