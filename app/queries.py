from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.model import User, CleanedData 


def get_licence_plates(db):
    with Session(db.engine) as session:  
        statement=select(CleanedData.license_plate, CleanedData.product_type_name, func.count().label("count")).group_by(CleanedData.license_plate,CleanedData.product_type_name)
        rows = session.execute(statement).all()
        return rows


    