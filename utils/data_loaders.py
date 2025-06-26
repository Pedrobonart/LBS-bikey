import pandas as pd
import geopandas as gpd
from pathlib import Path
import streamlit as st
from shapely import wkt
import json
import os

@st.cache_data
def get_stations_data():
    DATA_FILENAME = Path(__file__).parent.parent / 'data/bike_tracking_stations.csv'
    return pd.read_csv(DATA_FILENAME)

def load_bike_trips():
    return pd.read_csv("data/bike_journeys_noOutliers.csv")


@st.cache_data
def load_bezirke():
    df = pd.read_csv(Path(__file__).parent.parent / "data/BEZIRKSGRENZEOGD.csv")
    df_poly = df[df['SHAPE'].str.startswith('POLYGON')].copy()
    df_poly['geometry'] = df_poly['SHAPE'].apply(wkt.loads)
    gdf = gpd.GeoDataFrame(df_poly, geometry='geometry')
    gdf.set_crs(epsg=31256, inplace=True)
    return gdf.to_crs(epsg=4326)

@st.cache_data
def load_network_data():
    return pd.read_csv(Path(__file__).parent.parent / "data/network_extended.csv")

@st.cache_data
def load_balance_data():
    return pd.read_csv(Path(__file__).parent.parent / "data/station_dep_vs_arr (1).csv")

@st.cache_data
def load_time_of_day_data():
    return pd.read_csv(Path(__file__).parent.parent / "data/station_arr_dep_time (1).csv")

@st.cache_data
def load_trajectories_data():
    geojson_path = Path(__file__).parent.parent / 'data/agg_dur_traj (1).geojson'
    with open(geojson_path, "r", encoding="utf-8") as f:
        return json.load(f)
