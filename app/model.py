from flask_login import UserMixin
from app.app import db
from sqlalchemy import Column, Integer, String, Float, Boolean, BigInteger
from sqlalchemy.schema import Sequence

class User(db.Model, UserMixin):
    
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    isVerified = db.Column(db.Boolean, nullable=False, default=False, server_default='false')
    uploads = db.relationship('CleanedData', back_populates='user')

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.isVerified = False

class CleanedData(db.Model):
    __tablename__ = 'cleaned_data'   
    
    
    id = Column(db.BigInteger, Sequence('cleaned_data_id_seq'), primary_key=True, autoincrement=True)
    user_id = Column(Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='uploads')    
    city_id = Column(Integer)
    product_type_name = Column(String)
    global_product_name = Column(String)
    request_unix_time = Column(Integer)
    begintrip_unix_time = Column(Integer)
    dropoff_unix_time = Column(Integer)
    trip_day_of_year = Column(Integer)
    trip_day_of_week = Column(Integer)
    trip_month_of_year = Column(Integer)
    trip_hour_of_day = Column(Integer)
    actual_wait_time = Column(Float)
    wait_time_delta = Column(Float)
    begintrip_lat = Column(Float) 
    begintrip_lng = Column(Float) 
    dropoff_lat = Column(Float) 
    dropoff_lng = Column(Float)    
    driver_pickup_eta = Column(Integer)
    surge_multiplier = Column(Float)
    is_surged = Column(Boolean)
    has_destination = Column(Boolean)
    is_pool_matched = Column(Boolean)
    trip_distance_miles = Column(Float)
    trip_duration_seconds = Column(Integer)
    status = Column(String)
    is_completed = Column(Boolean)
    is_flat_rate = Column(Boolean)
    is_cash_trip = Column(Boolean)
    promotion_local = Column(Float)
    credits_local = Column(Float)
    has_driver_upfront_fare = Column(Boolean)
    driver_upfront_fare_local = Column(Float)
    original_fare_local = Column(Float)
    base_fare_local = Column(Float)
    surge_fare_local = Column(Float)
    minimum_fare_roundup_local = Column(Float)
    minimum_fare_roundup_usd = Column(Float)
    per_mile_fare_local = Column(Float)
    per_minute_fare_local = Column(Float)
    cancellation_fee_local = Column(Float)
    service_fee_local = Column(Float)
    toll_amount_local = Column(Float)
    booking_fee_local = Column(Float)
    earnings_boost_local = Column(Float)
    fare_distance_miles = Column(Float)
    fare_duration_minutes = Column(Float)
    wait_time_fare_local = Column(Float)
    service_fee = Column(Float)
    driver_cancellation_reason = Column(String)
    is_multidestination = Column(Boolean)
    driver_surge_multiplier = Column(Float)
    long_distance_surcharge_local = Column(Float)
    guaranteed_surge_multiplier = Column(Float)
    ufp_type = Column(String)
    cancellation_type = Column(String)
    is_directed_dispatch_trip = Column(Boolean)
    wait_duration_minutes = Column(Float)
    concierge_source_type = Column(String)
    is_scheduled_trip = Column(Boolean)
    is_airport_trip = Column(Boolean)
    license_plate = Column(String)
        