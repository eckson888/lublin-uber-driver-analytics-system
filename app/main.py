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

project_root = Path(__file__).resolve().parent.parent
merged_data_dir = project_root / "data" / "merged"
dataset = pd.read_csv(f"{merged_data_dir}/combined_cleaned_dataset.csv",encoding='cp1250', sep=",")
main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')


@main.route('/explore')
@login_required
def explore_plots():   
    
    plot_categories = ep.licence_plates_categories(dataset)
    plot_categories_html = pio.to_html(plot_categories, full_html=False, include_plotlyjs='cdn')
    
    plot_calendar = ep.calendar_summary(dataset)
    plot_calendar_html = pio.to_html(plot_calendar, full_html=False, include_plotlyjs='cdn')
    
    plot_median = ep.median_trip_costs(dataset)
    plot_median_html = pio.to_html(plot_median, full_html=False, include_plotlyjs='cdn')
    
    plot_average = ep.average_earnings_per_driver(dataset)
    plot_average_html = pio.to_html(plot_average, full_html=False, include_plotlyjs='cdn')
    
    plot_pickups_gradient = ep.pickups_heatmap(dataset)
    plot_pickups_gradient_html = pio.to_html(plot_pickups_gradient, full_html=False, include_plotlyjs='cdn')
    
    plot_dropoffs_scatter = ep.dropoffs_scatter(dataset)
    plot_dropoffs_scatter_html = pio.to_html(plot_dropoffs_scatter, full_html=False, include_plotlyjs='cdn')
    
    return render_template("explore.html",
                           plot_categories=plot_categories_html,
                           plot_calendar=plot_calendar_html,
                           plot_median=plot_median_html,
                           plot_average=plot_average_html,
                           plot_pickups_gradient=plot_pickups_gradient_html,
                           plot_dropoffs_scatter=plot_dropoffs_scatter_html)


