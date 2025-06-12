import streamlit as st
import pandas as pd
import math
from pathlib import Path
import folium
from streamlit_folium import st_folium

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='GDP dashboard',
    page_icon=':earth_americas:', # This is an emoji shortcode. Could be a URL too.
)

@st.cache_data
def get_stations_data():
    DATA_FILENAME = Path(__file__).parent / 'data/bike_tracking_stations.csv'
    return pd.read_csv(DATA_FILENAME)

# load & filter data
stations_df = get_stations_data()
stations_df = stations_df[~stations_df["place_name"].str.startswith("BIKE")]

st.markdown("This map shows the current locations of all bike stations in Vienna.")

# create map
map_center = [stations_df["lat"].mean(), stations_df["long"].mean()]
bike_map = folium.Map(location=map_center, zoom_start=13)

for _, row in stations_df.iterrows():
    folium.Marker(
        location=[row["lat"], row["long"]],
        popup=row["place_name"],
        icon=folium.Icon(color="blue", icon="bicycle", prefix="fa")
    ).add_to(bike_map)

# show map
st_folium(bike_map, width=700, height=500)
