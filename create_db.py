from app.app import create_app, db
from sqlalchemy import text
from app.model import User 

app = create_app()

with app.app_context():       
    
    print("Using database URI:", app.config['SQLALCHEMY_DATABASE_URI'])
    db.drop_all() 
    db.create_all()  
    db.session.commit()
    print("Database tables created!")
