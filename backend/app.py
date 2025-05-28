from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_required
from flask_migrate import Migrate 
from flask_session import Session
from flask_cors import CORS
from dotenv import load_dotenv
from models.models import db, User
from auth.routes import register_routes
from api.assistant_api import assistant_api_bp
from api.progress_api import progress_api
from auth.quiz_routes import quiz_bp
from admin.routes import admin_bp
import os



# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config.from_pyfile('config.py')

# --- Initialize Extensions with app instance ---
CORS(app) # Initialize Flask-CORS with the app
# Allows the flask_session folder created in backend folder
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = os.path.join(app.root_path, 'flask_session')  # inside backend folder
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
Session(app) # Initialize Flask-Session with the app

# Setup extensions
db.init_app(app)

# --- NEW: Initialize Flask-Migrate ---
migrate = Migrate(app, db) 

# Setup login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))  # SQLAlchemy 2.x safe

# Register blueprints
register_routes(app)  
app.register_blueprint(assistant_api_bp, url_prefix='/api')
app.register_blueprint(progress_api)
app.register_blueprint(quiz_bp, url_prefix='/api')
app.register_blueprint(admin_bp)

# Views
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index')
# @login_required
def index():
    return render_template('index.html')

# Run app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("✅ Database created.")
    app.run(debug=True)


