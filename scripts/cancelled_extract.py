import numpy as np
import pandas as pd

def extract_cancelled_trips(dataset):
    datasets_combined = dataset.copy() 
       
    drop_columns=["city_id","currency_code","timezone","flow","request_timestamp_utc","begintrip_timestamp_utc","dropoff_timestamp_utc",
                "promotion_usd","credits_usd","driver_upfront_fare_usd","original_fare_usd","base_fare_usd","surge_fare_usd","minimum_fare_roundup_usd",
                "per_mile_fare_usd","per_minute_fare_usd","cancellation_fee_usd","rounding_down_amount_usd","service_fee_usd","toll_amount_usd",
                "booking_fee_usd","earnings_boost_usd","wait_time_fare_usd","long_distance_surcharge_usd","vehicle_trip_number","cancellation_fee_local","driver_trip_number"]

    for column in drop_columns:
        datasets_combined.drop(column, axis='columns', inplace=True)

    md_cancelled_trips = pd.DataFrame(columns=datasets_combined.columns)
    cancelled_rows = datasets_combined[datasets_combined['is_completed'].astype(str) == 'False']
    md_cancelled_trips = cancelled_rows.copy()
    datasets_combined = datasets_combined[datasets_combined['is_completed'] != False]
    
    return md_cancelled_trips