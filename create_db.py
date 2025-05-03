from app.app import create_app, db
from sqlalchemy import text
from app.model import User 

app = create_app()

with app.app_context():       
    
    print("Using database URI:", app.config['SQLALCHEMY_DATABASE_URI'])
    # Drop all existing tables (use with caution!)
    db.drop_all()  # Be careful with this in production!
    db.create_all()  # Create the tables again
    db.session.commit()
    print("Database tables created!")
