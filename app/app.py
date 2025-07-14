import os
from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

load_dotenv()
login_manager = LoginManager()
app = Flask(__name__)
app.secret_key = 'dev'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("POSTGRES_URI")
db = SQLAlchemy(app)

def create_app():       
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TEMPLATES_AUTO_RELOAD'] = True 
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["SQLALCHEMY_RECORD_QUERIES"] = True     

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login' 
    
    from app.model import User
    
    with app.app_context():db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth
    app.register_blueprint(auth)    
        
    from .main import main
    app.register_blueprint(main)    
    
    from .verify import verify
    app.register_blueprint(verify)   
        
    return app