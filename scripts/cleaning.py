import numpy as np
import pandas as pd

def clean_data(datasets_combined):
    datasets_combined = datasets_combined.copy() 
       
    drop_columns=["city_id","currency_code","timezone","flow","request_timestamp_utc","begintrip_timestamp_utc","dropoff_timestamp_utc",
                "promotion_usd","credits_usd","driver_upfront_fare_usd","original_fare_usd","base_fare_usd","surge_fare_usd","minimum_fare_roundup_usd",
                "per_mile_fare_usd","per_minute_fare_usd","cancellation_fee_usd","rounding_down_amount_usd","service_fee_usd","toll_amount_usd",
                "booking_fee_usd","earnings_boost_usd","wait_time_fare_usd","long_distance_surcharge_usd","vehicle_trip_number","cancellation_fee_local","driver_trip_number"]

    for column in drop_columns:
        datasets_combined.drop(column, axis='columns', inplace=True)

    datasets_combined = datasets_combined[datasets_combined['is_completed'] != False]
    
    #time feature engineering

    datasets_combined.rename(columns={'eta': 'driver_pickup_eta'}, inplace=True)
        
    new_time_features=["request_unix_time","begintrip_unix_time","dropoff_unix_time",
                    "trip_day_of_year","trip_day_of_week","trip_month_of_year","trip_hour_of_day","actual_wait_time"]

    for c in new_time_features:
        datasets_combined[c]=0

    datasets_combined['request_unix_time'] = pd.to_datetime(datasets_combined['request_timestamp_local'],format='mixed').astype('int64') // 10**9
    datasets_combined['begintrip_unix_time'] = pd.to_datetime(datasets_combined['begintrip_timestamp_local'],format='mixed').astype('int64') // 10**9
    datasets_combined['dropoff_unix_time'] = pd.to_datetime(datasets_combined['dropoff_timestamp_local'],format='mixed').astype('int64') // 10**9
    datasets_combined['trip_day_of_year'] = pd.to_datetime(datasets_combined['begintrip_timestamp_local'], format='mixed').dt.day_of_year
    datasets_combined['trip_day_of_week'] = pd.to_datetime(datasets_combined['begintrip_timestamp_local'], format='mixed').dt.day_of_week
    datasets_combined['trip_month_of_year'] = pd.to_datetime(datasets_combined['begintrip_timestamp_local'], format='mixed').dt.month
    datasets_combined['trip_hour_of_day'] = pd.to_datetime(datasets_combined['begintrip_timestamp_local'], format='mixed').dt.hour    
    datasets_combined['actual_wait_time'] = (pd.to_datetime(datasets_combined['begintrip_timestamp_local'],format='mixed') - 
                                             pd.to_datetime(datasets_combined['request_timestamp_local'],format='mixed')).dt.total_seconds()
    datasets_combined['wait_time_delta'] = datasets_combined['actual_wait_time'] - datasets_combined['driver_pickup_eta']   


    # data cleaning/dimension reduction
    
    datasets_combined.drop("status", axis='columns', inplace=True)
    datasets_combined.drop("is_completed", axis='columns', inplace=True)
    datasets_combined.drop("global_product_name", axis='columns', inplace=True)
    datasets_combined.drop("has_destination", axis='columns', inplace=True)
    datasets_combined.drop("is_pool_matched", axis='columns', inplace=True)
    datasets_combined.drop("is_flat_rate", axis='columns', inplace=True)
    datasets_combined.drop("rounding_down_amount_local", axis='columns', inplace=True)
    datasets_combined.drop("booking_fee_local", axis='columns', inplace=True)
    datasets_combined.drop("toll_amount_local", axis='columns', inplace=True)
    datasets_combined.drop("earnings_boost_local", axis='columns', inplace=True)
    datasets_combined.drop("driver_cancellation_reason", axis='columns', inplace=True)
    datasets_combined.drop("guaranteed_surge_multiplier", axis='columns', inplace=True)
    datasets_combined.drop("cancellation_type", axis='columns', inplace=True)
    datasets_combined.drop("is_directed_dispatch_trip", axis='columns', inplace=True)

    datasets_combined['promotion_local'] = datasets_combined['promotion_local'].replace({'\\N': '0'})
    datasets_combined['promotion_local'] = datasets_combined['promotion_local'].fillna('0')
    datasets_combined['service_fee_local'] = datasets_combined['service_fee_local'].replace({'\\N': '0'})
    datasets_combined['service_fee_local'] = datasets_combined['service_fee_local'].fillna('0')
    datasets_combined['wait_time_fare_local'] = datasets_combined['wait_time_fare_local'].replace({'\\N': '0'})
    datasets_combined['wait_time_fare_local'] = datasets_combined['wait_time_fare_local'].fillna('0')
    datasets_combined['long_distance_surcharge_local'] = datasets_combined['long_distance_surcharge_local'].replace({'\\N': '0'})
    datasets_combined['long_distance_surcharge_local'] = datasets_combined['long_distance_surcharge_local'].fillna('0')
    datasets_combined['wait_duration_minutes'] = datasets_combined['wait_duration_minutes'].replace({'\\N': '0'})
    datasets_combined['wait_duration_minutes'] = datasets_combined['wait_duration_minutes'].fillna('0')
    datasets_combined['minimum_fare_roundup_local'] = datasets_combined['minimum_fare_roundup_local'].replace({'\\N': '0'})
    datasets_combined['minimum_fare_roundup_local'] = datasets_combined['minimum_fare_roundup_local'].fillna('0')
    datasets_combined['concierge_source_type'] = datasets_combined['concierge_source_type'].replace({'\\N': 'none'})
    datasets_combined['concierge_source_type'] = datasets_combined['concierge_source_type'].fillna('none')
    datasets_combined['credits_local'] = datasets_combined['credits_local'].replace({'\\N': '0'})
    datasets_combined['credits_local'] = datasets_combined['credits_local'].fillna('0')
    
    datasets_combined['surge_fare_local'] = datasets_combined['surge_fare_local'].fillna('0')
    datasets_combined['per_minute_fare_local'] = datasets_combined['per_minute_fare_local'].fillna('0')
    datasets_combined['fare_duration_minutes'] = datasets_combined['fare_duration_minutes'].fillna('0')
    datasets_combined['base_fare_local'] = datasets_combined['base_fare_local'].fillna('0')
    datasets_combined['service_fee'] = datasets_combined['service_fee'].fillna('0')
    datasets_combined['per_mile_fare_local'] = datasets_combined['per_mile_fare_local'].fillna('0')
    datasets_combined['original_fare_local'] = datasets_combined['original_fare_local'].fillna('0')
    datasets_combined['ufp_type'] = datasets_combined['ufp_type'].fillna('none')
    datasets_combined['fare_distance_miles'] = datasets_combined['fare_distance_miles'].fillna('0')

    datasets_combined['license_plate'] = datasets_combined['license_plate'].str.replace(r'\s+', '', regex=True)
    datasets_combined['license_plate'] = datasets_combined['license_plate'].fillna('\\N')
    datasets_combined['license_plate'] = datasets_combined['license_plate'].replace({'\\N': 'undefined'})
    
    #TODO: change this so it works with geo/api data    
    # if 'pickup_street' in datasets_combined.columns:
    #     datasets_combined['pickup_street'] = datasets_combined['pickup_street'].str.lower()
    #     datasets_combined['pickup_city'] = datasets_combined['pickup_city'].str.lower()
    #     datasets_combined['destination_street'] = datasets_combined['destination_street'].str.lower()
    #     datasets_combined['destination_city'] = datasets_combined['destination_city'].str.lower()      


    return datasets_combined