import pandas as pd
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.model import CleanedData 


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
    
def get_fares(db):
    with Session(db.engine) as session:
        statement=select(CleanedData.per_mile_fare_local, CleanedData.per_minute_fare_local,CleanedData.begintrip_unix_time,CleanedData.user_id)
        fares_and_dates=session.execute(statement).all()
        df = pd.DataFrame(fares_and_dates,columns=['per_mile_fare','per_minute_fare','begintrip_timestamp','driver_id'])
        return df

def get_trip_prices(db):
    with Session(db.engine) as session:
        statement=select(CleanedData.begintrip_unix_time,CleanedData.driver_upfront_fare_local,CleanedData.user_id)
        result = session.execute(statement).all()
        df = pd.DataFrame(result,columns=['begintrip_timestamp','driver_upfront_fare','driver_id'])
        return df
    
def get_locations(db):
    with Session(db.engine) as session:
        statement=select(CleanedData.begintrip_lat,CleanedData.begintrip_lng,CleanedData.dropoff_lat,CleanedData.dropoff_lng)
        result = session.execute(statement).all()
        df = pd.DataFrame(result,columns=['begintrip_lat','begintrip_lng','dropoff_lat','dropoff_lng'])
        return df