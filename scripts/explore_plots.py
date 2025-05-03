import os
import pandas as pd
import plotly as pt
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px

from plotly_calplot import calplot


def licence_plates_categories(dataset):    
    df_counts = dataset.groupby(['product_type_name', 'license_plate']).size().reset_index(name='count')
    df_counts_sorted = df_counts.sort_values(by='count', ascending=False)
    fig = px.bar(df_counts_sorted, 
                y='license_plate', 
                x='count', 
                color='product_type_name', 
                title="Categories realized by each car",
                labels={'product_type_name': 'Category', 'license_plate': 'License plate', 'count': 'Amount'},
                hover_data=['product_type_name', 'license_plate', 'count'],
                color_discrete_sequence=["#222222", "#999999", "#6f03fc", "#c800ff", "#ff005d","#3d0000"])
    fig.update_layout(height=500, plot_bgcolor='white')
    
    fig.update_xaxes(
        showline=True,
        linewidth=2,
        linecolor='black',
        mirror=True,
        showgrid=True,
        gridwidth=1,
        gridcolor='#bbbbbb')
    
    fig.update_yaxes(
        showline=True,
        linewidth=2,
        linecolor='black',
        mirror=True,
        showgrid=True,
        gridwidth=1,
        gridcolor='#bbbbbb')
    
    return fig

def calendar_summary(dataset_):
    dataset = dataset_.copy()
    
    dataset['begintrip_timestamp_local'] = pd.to_datetime(dataset['begintrip_timestamp_local'],format='mixed')
    dataset['day_of_year'] = dataset['begintrip_timestamp_local'].dt.day_of_year
    dataset = dataset.dropna(subset=['day_of_year'])
    dataset['day_of_year'] = dataset['day_of_year'].astype(int)

    day_of_year_counts = dataset.groupby('day_of_year').size().reset_index(name='count')
    reference_year = 2025
    day_of_year_counts['date'] = pd.to_datetime(day_of_year_counts['day_of_year'].astype(str), format='%j')
    day_of_year_counts['date'] = day_of_year_counts['date'].apply(lambda x: x.replace(year=reference_year))


    fig = calplot(
        day_of_year_counts,  
        x='date',            
        y='count',
        title="Heatmap of each day in a year",
        colorscale='RdPu'
    )

    fig.update_layout(        
        font=dict(family='Arial', size=14, color='black'),
        height=500
        )
    
    
    return fig

def median_trip_costs(dataset_):
    dataset=dataset_.copy()
    dataset['begintrip_timestamp_local'] = pd.to_datetime(dataset['begintrip_timestamp_local'], format='mixed')
    month_mean_trip_costs = dataset.groupby(dataset.begintrip_timestamp_local.dt.to_period('M'))['driver_upfront_fare_local'].mean().reset_index(name='Monthly Mean')
    month_mean_trip_costs = month_mean_trip_costs.sort_values(by='begintrip_timestamp_local', ascending=True)
    month_mean_trip_costs['begintrip_timestamp_local'] = month_mean_trip_costs['begintrip_timestamp_local'].dt.strftime('%b %Y')
    month_mean_trip_costs = month_mean_trip_costs.rename(columns={"begintrip_timestamp_local": "Month_Year"})
    
    fig = px.line(data_frame=month_mean_trip_costs,x='Month_Year',y="Monthly Mean",title="Median of trip prices across months")
    fig.update_traces(line_color='#000000')
    fig.update_layout(height=500, font=dict(family='Arial', size=14, color='black'),plot_bgcolor="#999999")
    return fig

def average_earnings_per_driver(dataset_):
    dataset = dataset_.copy()
    
    dataset['begintrip_timestamp_local']=pd.to_datetime(dataset['begintrip_timestamp_local'], format='mixed')
    
    grouped = dataset.groupby(dataset.begintrip_timestamp_local.dt.to_period('M'))
    month_avg_earnings = grouped['driver_upfront_fare_local'].sum() / grouped['driver_id'].nunique()
    month_avg_earnings = month_avg_earnings.reset_index(name='Monthly Average')
    month_avg_earnings = month_avg_earnings.sort_values(by='begintrip_timestamp_local', ascending=True)
    month_avg_earnings['begintrip_timestamp_local'] = month_avg_earnings['begintrip_timestamp_local'].dt.strftime('%b %Y')

    fig = px.line(
        data_frame=month_avg_earnings,
        x='begintrip_timestamp_local',
        y="Monthly Average",
        title="Average monthly earnings per driver")

    fig.update_traces(line_color='#000000')
    fig.update_layout(height=500, font=dict(family='Arial', size=14, color='black'),plot_bgcolor="#999999")
    return fig

def pickups_heatmap(dataset_):
    dataset = dataset_.copy()
    grouped = dataset.groupby(["begintrip_lat", "begintrip_lng"]).size().reset_index(name="count")
    grouped['count_impr'] = np.sqrt(grouped['count'].astype(float))

    fig = px.density_map(
        data_frame=grouped,
        lat="begintrip_lat",
        lon="begintrip_lng",
        z="count_impr",
        opacity=0.8,
        zoom=12,
        radius=130,
        custom_data="count",
        map_style='carto-darkmatter',
        title="Pickup locations heatmap"
    )

    fig.update_layout(
        
        height=700,
        font=dict(family='Arial', size=14, color='black'),
    )

    fig.update_traces(
        hovertemplate=(
            'Latitude: %{lat}<br>'
            'Longitude: %{lon}<br>'        
            'Amount of pickups from this location: %{customdata[0]}<extra></extra>'
        )
    )

    return fig

def dropoffs_scatter(dataset_):
    dataset=dataset_.copy()
    grouped = dataset.groupby(["dropoff_lat", "dropoff_lng"]).size().reset_index(name="Dropoffs in this location")
    grouped['size'] = 50
    grouped['count_impr'] = np.sqrt(grouped['Dropoffs in this location'].astype(float))

    fig = px.scatter_map(
        data_frame=grouped,
        lat="dropoff_lat",
        lon="dropoff_lng",
        color="count_impr",
        size="size",
        opacity=0.8,
        zoom=10,
        hover_data="Dropoffs in this location",
        map_style='dark',
        title="Dropoff Locations scatter heatmap"
    )

    fig.update_layout(
        height=700,
        font=dict(family='Arial', size=14, color='black'),
        legend_visible=False
    )

    return fig

