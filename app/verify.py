import pandas as pd
import numpy as np
from scripts import cleaning
from scripts import cancelled_extract
from app.app import db
from app.model import CleanedData
from io import StringIO
from app.exceptions import DuplicateTripError
from pathlib import Path
from sqlalchemy import select, tuple_, MetaData, Table
from scripts import explore_plots as ep
from sqlalchemy.exc import SQLAlchemyError
from flask import Blueprint, render_template
from flask import request, redirect, url_for, render_template, flash
from flask_login import login_required, current_user

verify = Blueprint('verify', __name__)
project_root = Path(__file__).resolve().parent.parent
merged_data_dir = project_root / "data" / "merged"
raw_cols = [column.name for column in CleanedData.__table__.columns]


def clean_uploaded_file(file_stream):
    df = pd.read_csv(StringIO(file_stream.read().decode('utf-8')),na_values="\\N",encoding='cp1250') 
    cleaned_df = cleaning.clean_data(df)       
    return cleaned_df

def normalize_file_types(dataframe):
    df = dataframe
    
    type_mapping = {
        'city_id': 'Int64',
        'product_type_name': 'string',
        'global_product_name': 'string',
        'request_unix_time': 'Int64',
        'begintrip_unix_time': 'Int64',
        'dropoff_unix_time': 'Int64',
        'trip_day_of_year': 'Int64',
        'trip_day_of_week': 'Int64',
        'trip_month_of_year': 'Int64',
        'trip_hour_of_day': 'Int64',
        'actual_wait_time': 'float64',
        'wait_time_delta': 'float64',
        'begintrip_lat': 'float64',
        'begintrip_lng': 'float64',
        'dropoff_lat': 'float64',
        'dropoff_lng': 'float64',
        'driver_pickup_eta': 'Int64',
        'surge_multiplier': 'float64',
        'is_surged': 'boolean',
        'has_destination': 'boolean',
        'is_pool_matched': 'boolean',
        'trip_distance_miles': 'float64',
        'trip_duration_seconds': 'Int64',
        'status': 'string',
        'is_completed': 'boolean',
        'is_flat_rate': 'boolean',
        'is_cash_trip': 'boolean',
        'promotion_local': 'float64',
        'credits_local': 'float64',
        'has_driver_upfront_fare': 'boolean',
        'driver_upfront_fare_local': 'float64',
        'original_fare_local': 'float64',
        'base_fare_local': 'float64',
        'surge_fare_local': 'float64',
        'minimum_fare_roundup_local': 'float64',
        'minimum_fare_roundup_usd': 'float64',
        'per_mile_fare_local': 'float64',
        'per_minute_fare_local': 'float64',
        'cancellation_fee_local': 'float64',
        'service_fee_local': 'float64',
        'toll_amount_local': 'float64',
        'booking_fee_local': 'float64',
        'earnings_boost_local': 'float64',
        'fare_distance_miles': 'float64',
        'fare_duration_minutes': 'float64',
        'wait_time_fare_local': 'float64',
        'service_fee': 'float64',
        'driver_cancellation_reason': 'string',
        'is_multidestination': 'boolean',
        'driver_surge_multiplier': 'float64',
        'long_distance_surcharge_local': 'float64',
        'guaranteed_surge_multiplier': 'float64',
        'ufp_type': 'string',
        'cancellation_type': 'string',
        'is_directed_dispatch_trip': 'boolean',
        'wait_duration_minutes': 'float64',
        'concierge_source_type': 'string',
        'is_scheduled_trip': 'boolean',
        'is_airport_trip': 'boolean',
        'license_plate': 'string'}

    for col, dtype in type_mapping.items():
        if col in df.columns:
            try:
                df[col] = df[col].astype(dtype)
            except Exception as e:
                print(f"Error converting column '{col}' to {dtype}: {e}")
                
    for col in df.select_dtypes(include='float'):
        df[col] = df[col].round(5)

    return df


def get_existing_keys(pairs,table, batch_size=500):
    existing = set()
    for i in range(0, len(pairs), batch_size):
        batch = pairs[i:i + batch_size]
        stmt = select(table.c.begintrip_unix_time, table.c.license_plate).where(tuple_(table.c.begintrip_unix_time, table.c.license_plate).in_(batch))
        
        with db.engine.connect() as conn:
            result = conn.execute(stmt)
            existing.update(result.fetchall())
    return existing

def verify_upload(uploaded_dataframe):

    from app.exceptions import DuplicateTripError
    
    df = uploaded_dataframe    
    metadata = MetaData()
    cleaned_data = Table("cleaned_data", metadata, autoload_with=db.engine)       
    key_pairs = df[['begintrip_unix_time', 'license_plate']].dropna()
    
    pairs = [
    (int(row['begintrip_unix_time']), str(row['license_plate']))
    for _, row in key_pairs.iterrows()
]

    if not pairs:
        raise ValueError("Brak odpowiednich par kluczy w pliku CSV")
        
    duplicates = get_existing_keys(pairs,cleaned_data,500)        

    if duplicates:
        raise DuplicateTripError("Plik CSV zawiera istniejące już dane. Proszę przesłać nowy plik od Ubera.")    
    
    matching = set(df.columns) & set(raw_cols)    
    if not matching:
        return None  

    extra = set(df.columns) - set(raw_cols)
    if extra:
        df = df.drop(columns=extra)
        
    df = df.reindex(columns=raw_cols)
    return df


@verify.route('/upload', methods=['GET','POST'])
@login_required
def upload():
    error = None
    if current_user.isVerified:        
        return redirect(url_for('main.home'))    
    
    if request.method == 'POST':
        file = request.files.get('data_file')
        error = None
        
        if not file or not file.filename.endswith('.csv'):
            error = "Proszę wysłać plik CSV pobrany od Ubera."
        else:
            try:
                cleaned_df = clean_uploaded_file(file.stream)
                normalized_df = normalize_file_types(cleaned_df)
                df = verify_upload(normalized_df)
                if df is None:
                    error = "Proszę wysłać oryginalny plik CSV pobrany od Ubera."
                else:
                    df['user_id'] = current_user.id
                    if 'id' in df.columns:
                        df = df.drop(columns=['id'])
                    records = df.to_dict(orient='records')
                    cleaned_data_objects = [CleanedData(**record) for record in records]          
                    current_user.isVerified = True
                    db.session.add_all(cleaned_data_objects)
                    db.session.commit()
                    flash("Twoje konto zostało pomyślnie zweryfikowane.", "success")
                    return redirect(url_for('main.home'))

            except DuplicateTripError as e:
                error = str(e)
            
            except SQLAlchemyError as e:
                error = f"Błąd bazy danych: {e}" 
                
            except Exception as e:
                error = f"Wystąpił nieoczekiwany błąd: {str(e)}"

    return render_template('upload.html', error=error)