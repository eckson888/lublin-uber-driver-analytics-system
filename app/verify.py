import pandas as pd
import plotly.io as pio

from app.app import db
from io import StringIO
from app.model import User
from app.exceptions import DuplicateTripError
from pathlib import Path
from sqlalchemy import select, tuple_, MetaData, Table
from sqlalchemy.sql import text
from scripts import explore_plots as ep
from sqlalchemy.exc import SQLAlchemyError
from flask import Blueprint, render_template
from werkzeug.security import check_password_hash
from flask import request, redirect, url_for, render_template, flash
from flask_login import login_user, logout_user, login_required, current_user

verify = Blueprint('verify', __name__)
project_root = Path(__file__).resolve().parent.parent
merged_data_dir = project_root / "data" / "merged"
raw_cols = pd.read_csv(f"{merged_data_dir}/combined_dataset.csv",encoding='cp1250', sep=",",na_values="\\N", low_memory=False).columns

def get_existing_keys(pairs,table, batch_size=500):
    existing = set()
    for i in range(0, len(pairs), batch_size):
        batch = pairs[i:i + batch_size]
        stmt = select(table.c.begintrip_timestamp_local,table.c.license_plate).where(tuple_(table.c.begintrip_timestamp_local, table.c.license_plate).in_(batch))
        
        with db.engine.connect() as conn:
            result = conn.execute(stmt)
            existing.update(result.fetchall())
    return existing

def normalize_upload(file_stream):

    from app.exceptions import DuplicateTripError
    
    df = pd.read_csv(StringIO(file_stream.read().decode('utf-8')),na_values="\\N")     
    metadata = MetaData()
    raw_data = Table("raw_data", metadata, autoload_with=db.engine)       
    key_pairs = df[['begintrip_timestamp_local', 'license_plate']].dropna()
    pairs = [tuple(x) for x in key_pairs.to_records(index=False)]

    if not pairs:
        raise ValueError("No valid keys found in CSV")
        
    duplicates = get_existing_keys(pairs,raw_data,500)        

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
        flash("Your account is already verified!", "info")
        return redirect(url_for('main.home'))    
    
    if request.method == 'POST':
        file = request.files.get('data_file')
        error = None
        
        if not file or not file.filename.endswith('.csv'):
            error = "Proszę wysłać plik CSV pobrany od Ubera."
        else:
            try:
                df = normalize_upload(file.stream)
                if df is None:
                    error = "Proszę wysłać oryginalny plik CSV pobrany od Ubera."
                else:
                    df['user_id'] = current_user.id
                    df.to_sql('raw_data', db.engine, if_exists='append', index=False)
                    current_user.isVerified = True
                    db.session.commit()
                    flash("Twoje konto zostało pomyślnie zweryfikowane.", "success")
                    return redirect(url_for('main.home'))

            except DuplicateTripError as e:
                error = str(e)
            #TODO wyjebac to poznie
            except SQLAlchemyError as e:
                error = f"Błąd bazy danych: {e}" 
                
            except Exception as e:
                error = f"Wystąpił nieoczekiwany błąd: {str(e)}"

    return render_template('upload.html', error=error)