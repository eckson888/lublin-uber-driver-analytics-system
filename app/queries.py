import pandas as pd
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.model import User, CleanedData 


def get_licence_plates(db):
    with Session(db.engine) as session:  
        statement=select(CleanedData.license_plate, CleanedData.product_type_name, func.count().label("count")).group_by(CleanedData.license_plate,CleanedData.product_type_name)
        rows = session.execute(statement).all()
        df = pd.DataFrame(rows, columns=['license_plate', 'product_type_name','count'])
        return df

def get_trip_calendar(db):
    with Session(db.engine) as session:
        statement=select(CleanedData.begintrip_unix_time,CleanedData.user_id)
        time_and_drivers=session.execute(statement).all()
        df = pd.DataFrame(time_and_drivers, columns=['begintrip_timestamp', 'driver_id'])
        return df
    