import streamlit as st
from utils.data_loaders import load_trajectories_data
import folium
from streamlit_folium import st_folium
import json
import branca.colormap as cm
import pandas as pd

def show_page():
    st.header("In-depth Analysis")
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        st.markdown("### Movement Flow Map")
        st.write("""
        This interactive map shows **aggregated nighttime bike trips** in Vienna.  
        Each line represents a movement from an origin to a destination station.
        """)
        st.markdown("### Visual Encoding")
        st.write("""
        - **Line color**: Represents the average trip duration.
        - **Line width**: Corresponds to how many trips occurred on that route.
        """)
        st.markdown("### Use This Map To:")
        st.write("""
        - Identify long vs. short duration trips  
        - Spot frequently used corridors  
        - Understand spatial usage patterns at night
        """)

    with col2:
        geojson_data = load_trajectories_data()

        durations = [feat["properties"]["avg_duration_min"] for feat in geojson_data["features"]]
        min_dur = min(durations)
        max_dur = max(durations)

        colormap = cm.linear.YlOrRd_09.scale(min_dur, max_dur)
        colormap.caption = "Average Trip Duration (min)"

        origins = [(f["properties"]["origin_lat"], f["properties"]["origin_lon"]) for f in geojson_data["features"]]
        avg_lat = sum([lat for lat, _ in origins]) / len(origins)
        avg_lon = sum([lon for _, lon in origins]) / len(origins)

        m = folium.Map(location=[avg_lat, avg_lon], zoom_start=12)

        for feature in geojson_data["features"]:
            coords = feature["geometry"]["coordinates"]
            props = feature["properties"]
            duration = props["avg_duration_min"]
            count = props["trip_count"]
            color = colormap(duration)

            popup_text = f"""
            <b>Trips:</b> {count}<br>
            <b>Avg Duration:</b> {duration:.2f} min
            """

            folium.PolyLine(
                locations=[(lat, lon) for lon, lat in coords],
                color=color,
                weight=0.7 + count * 0.8,
                opacity=0.7,
                popup=folium.Popup(popup_text, max_width=300)
            ).add_to(m)

        colormap.add_to(m)
        st_folium(m, width=700, height=500)

    with col3:
        st.markdown("### Notes")
        st.write("""
        This dataset only includes trips recorded during **nighttime hours** (e.g., 10 PM–6 AM).  
        It has been **pre-aggregated** by origin/destination coordinates.
        """)
