import os
import pandas as pd

import plotly as pt
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from plotly_calplot import calplot


def licence_plates_categories(dataset):    
    # df_counts = dataset.groupby(['product_type_name', 'license_plate']).size().reset_index(name='count')
    df_counts_sorted = dataset.sort_values(by='count', ascending=False)
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
    
    dataset['begintrip_timestamp'] = pd.to_datetime(dataset['begintrip_timestamp'], unit='s').dt.date
    trips_per_driver_day = dataset.groupby(['begintrip_timestamp', 'driver_id']).size().reset_index(name='trips')
    trips_per_driver_day['year'] = pd.to_datetime(trips_per_driver_day['begintrip_timestamp']).dt.year
    
    daily_medians = trips_per_driver_day.groupby(['begintrip_timestamp', 'year']).agg(
        median_trips_per_driver=('trips', 'median'),
        driver_count=('driver_id', 'count')
    ).reset_index()
    

    fig = calplot(
        daily_medians,  
        x='begintrip_timestamp',            
        y='median_trips_per_driver',
        title="Mediana przejazdów na kierowce w kazdy dzien",
        colorscale='RdPu'
    )

    fig.update_layout(        
        font=dict(family='Arial', size=14, color='black'),
        height=800
        )   

    
    return fig

def median_trip_costs(dataset_):    
    
    dataset=dataset_.copy()
    dataset['per_km_fare'] = dataset['per_mile_fare'] / 1.60934
    dataset['begintrip_timestamp'] = pd.to_datetime(dataset['begintrip_timestamp'], unit='s')
    
    month_mean_per_mile_fare = dataset.groupby(dataset.begintrip_timestamp.dt.to_period('M'))['per_km_fare'].mean().reset_index(name='zł/km')    
    month_mean_per_mile_fare = month_mean_per_mile_fare.sort_values(by='begintrip_timestamp', ascending=True)
    month_mean_per_mile_fare['begintrip_timestamp'] = month_mean_per_mile_fare['begintrip_timestamp'].dt.strftime('%b %Y')
    month_mean_per_mile_fare = month_mean_per_mile_fare.rename(columns={"begintrip_timestamp": "Miesiac/Rok"})
    
    # month_mean_per_minute_fare = dataset.groupby(dataset.begintrip_timestamp.dt.to_period('M'))['per_minute_fare'].mean().reset_index(name='Monthly Per Minute Mean')
    # month_mean_per_minute_fare = month_mean_per_minute_fare.sort_values(by='begintrip_timestamp', ascending=True)
    # month_mean_per_minute_fare['begintrip_timestamp'] = month_mean_per_minute_fare['begintrip_timestamp'].dt.strftime('%b %Y')
    # month_mean_per_minute_fare = month_mean_per_minute_fare.rename(columns={"begintrip_timestamp": "Month_Year"})
    
    fig = px.line(
        data_frame=month_mean_per_mile_fare,
        x='Miesiac/Rok',
        y="zł/km",
        title="Mediana stawek za km na przestrzeni miesiecy"
        
    )

    # fig.add_trace(
    #     go.Scatter(
    #         x=month_mean_per_minute_fare['Month_Year'],
    #         y=month_mean_per_minute_fare['Monthly Per Minute Mean'],
    #         mode='lines',
    #         name='Monthly Per Minute Mean',
    #         line=dict(color='blue')  # customize if needed
    #     )
    # )
    fig.update_yaxes(range=[1.0, 2.0])
    fig.update_traces(line_color='#ff005d')    
    fig.update_layout(
        height=500,
        font=dict(family='Arial', size=14, color='black'),
        plot_bgcolor="#aaaaaa",
        legend_title_text='Fare Type'
    )
    


    return fig

def average_earnings_per_driver(dataset_):
    dataset = dataset_.copy()
    
    dataset['begintrip_timestamp'] = pd.to_datetime(dataset['begintrip_timestamp'], unit='s')
    dataset['month'] = dataset['begintrip_timestamp'].dt.to_period('M')

    driver_monthly_totals = dataset.groupby(['month', 'driver_id'])['driver_upfront_fare'].sum().reset_index()

    monthly_avg = driver_monthly_totals.groupby('month')['driver_upfront_fare'].mean().reset_index(name='Monthly Average')
    monthly_avg['month'] = monthly_avg['month'].astype(str)    

    fig = px.line(
        data_frame=monthly_avg,
        x='month',
        y="Monthly Average",
        title="Średnie zarobki miesięczne netto")

    fig.update_traces(line_color='#6f03fc')
    fig.update_layout(height=600, font=dict(family='Arial', size=14, color='black'),plot_bgcolor="#999999")
    return fig

def average_daily_earnings_over_time(dataset_):
    dataset = dataset_.copy() 

    dataset['begintrip_timestamp'] = pd.to_datetime(dataset['begintrip_timestamp'], unit='s')
    dataset['month'] = dataset['begintrip_timestamp'].dt.to_period('M')
    dataset['trip_date'] = dataset['begintrip_timestamp'].dt.date

    daily_earnings = dataset.groupby(['driver_id', 'trip_date'])['driver_upfront_fare'].sum().reset_index()
    daily_earnings['month'] = pd.to_datetime(daily_earnings['trip_date']).dt.to_period('M')

    driver_monthly_avg = daily_earnings.groupby(['month', 'driver_id'])['driver_upfront_fare'].mean().reset_index()

    monthly_avg = driver_monthly_avg.groupby('month')['driver_upfront_fare'].mean().reset_index(name='Monthly Average')
    monthly_avg['month'] = monthly_avg['month'].dt.to_timestamp()

    fig = px.line(
        data_frame=monthly_avg,
        x='month',
        y="Monthly Average",
        title="Średnie zarobki dzienne netto")

    fig.update_traces(line_color="#000000")
    fig.update_layout(height=600, 
                      font=dict(family='Arial', size=14, color='black'),
                      plot_bgcolor="#999999",
                      xaxis=dict(
                                tickformat="%b\n%Y",  
                                dtick="M1"            
                                ))
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
        
        height=850,
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
        height=850,
        font=dict(family='Arial', size=14, color='black'),
        legend_visible=False
    )

    return fig


