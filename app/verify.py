import pandas as pd
import plotly.io as pio

from app.app import db
from io import StringIO
from app.model import User
from pathlib import Path
from scripts import explore_plots as ep
from sqlalchemy.exc import SQLAlchemyError
from flask import Blueprint, render_template
from werkzeug.security import check_password_hash
from flask import request, redirect, url_for, render_template, flash
from flask_login import login_user, logout_user, login_required, current_user

verify = Blueprint('verify', __name__)
project_root = Path(__file__).resolve().parent.parent
merged_data_dir = project_root / "data" / "merged"
raw_cols = pd.read_csv(f"{merged_data_dir}/combined_dataset.csv",encoding='cp1250', sep=",").columns

def normalize_upload(file_stream):

    df = pd.read_csv(StringIO(file_stream.read().decode('utf-8')))
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
        if not file or not file.filename.endswith('.csv'):
            error = "Prosze wysłać plik CSV pobrany od Ubera."
        else:
            df = normalize_upload(file.stream)
            if df is None:
                error = "Prosze wysłać oryginalny plik CSV pobrany od Ubera."
            else:
                df['user_id'] = current_user.id
                try:
                    df.to_sql('raw_data', db.engine, if_exists='append', index=False)
                    current_user.isVerified = True
                    db.session.commit()
                    flash("✅ Your account is now verified!", "success")
                    return redirect(url_for('main.explore_plots'))
                except SQLAlchemyError as e:
                    error = f"Database error: {e}"                

    return render_template('upload.html', error=error)
