import streamlit as st
from utils.data_loaders import load_bike_trips, load_bezirke
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import pandas as pd

def show_page():
    st.header("Heatmap")
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        st.markdown("### About the Project")
        st.write("""
        This interactive heatmap gives a good overview of the density of rental stations in Vienna.
        The monocentric structure of Vienna can be clearly seen.
        """)

    with col2:
        df = load_bike_trips()
        origins = df[["origin_lat", "origin_lon"]].copy()
        destinations = df[["destination_lat", "destination_lon"]].copy()
        origins.columns = ["lat", "lon"]
        destinations.columns = ["lat", "lon"]
        all_points = pd.concat([origins, destinations], ignore_index=True)
        heat_data = all_points.groupby(["lat", "lon"]).size().reset_index(name="count")
        heat_points = heat_data[["lat", "lon", "count"]].values.tolist()

        map_center = [df["origin_lat"].mean(), df["origin_lon"].mean()]
        heat_map = folium.Map(location=map_center, zoom_start=11, min_zoom=10)

        gdf = load_bezirke()
        folium.GeoJson(
            gdf,
            name="Vienna Districts",
            tooltip=folium.GeoJsonTooltip(fields=["NAMEK"], aliases=["District Name:"]),
            style_function=lambda feature: {
                "color": "#000000",
                "weight": 0.5,
                "fillOpacity": 0,
                "opacity": 0.35
            }
        ).add_to(heat_map)

        HeatMap(heat_points, radius=15, blur=20, max_zoom=1, opacity=0.8, gradient={
            0.0: '#ffffff', 0.333:'#ffd43b', 0.6667:'#ed6d0c', 1:'#a61c1c'
        }).add_to(heat_map)

        folium.LayerControl().add_to(heat_map)
        st_folium(heat_map, width=700, height=500)

    with col3:
        st.markdown("### More density info")
        st.write("""
        In the Central area inside the "Gürtel" (approx. 33 km²), there are 68 stations;
        while there are 186 stations in the peripheral area (approx. 381.6 km²).
        """)
        st.metric("Avg Stations per km^2 in city center", f"2.06")
        st.metric("Avg Stations per km^2 in city center", f"0.49")
