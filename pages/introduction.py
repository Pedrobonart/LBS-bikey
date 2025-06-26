import streamlit as st
from utils.data_loaders import get_stations_data, load_bike_trips
import folium
from streamlit_folium import st_folium
import pandas as pd

def show_page():
    stations_df = get_stations_data()
    stations_df = stations_df[~stations_df["place_name"].str.startswith("BIKE")]

    st.header("Introduction")
    st.markdown(
        """
        <div style="background-color:#f0f2f6; padding: 20px; border-radius: 10px; margin-bottom: 20px">
            <h1 style="color:#2C3E50;">🚲 Vienna Bike Sharing Dashboard</h1>
            <h4 style="color:#7f8c8d;">An interactive analysis of the WienMobil Rad system</h4>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1.5, 2, 1.5])

    with col1:
        st.markdown("### About the Project")
        st.write("""
        With cities growing rapidly, there’s an urgent need to rethink how we move through urban spaces. Making cities less dependent on cars is a key step toward more sustainable and inclusive living...
        """)

        st.markdown("### Data Overview")
        st.write("""
        The map shows the current locations of all bike stations in Vienna. There are 254 bike stations spread across the city, allowing people to rent bikes and ride them to other stations.
        Each marker represents one station. Clicking on it reveals the station name.
        """)

        st.markdown("### Sources")
        st.write("""
        - Source: [WienMobil Rad](https://www.wien.gv.at/english/transportation/bike/)
        - Data: scraped from the Nextbike API.
        """)

    with col2:
        map_center = [48.21204, 16.37733]
        bike_map = folium.Map(location=map_center, zoom_start=11, min_zoom=10)
        for _, row in stations_df.iterrows():
            folium.Marker(
                location=[row["lat"], row["long"]],
                popup=row["place_name"],
                icon=folium.Icon(color="blue", icon="bicycle", prefix="fa")
            ).add_to(bike_map)
        st_folium(bike_map, width=500, height=500)

    with col3:
        st.markdown("### Statistics")
        df = load_bike_trips()

        df["departure_time"] = pd.to_datetime(df["departure_time"])
        df["arrival_time"] = pd.to_datetime(df["arrival_time"])

        total_trips = len(df)
        avg_duration = df["duration_min"].mean()
        start_time = df["departure_time"].min()
        end_time = df["departure_time"].max()
        duration_hours = (end_time - start_time).total_seconds() / 3600
        unique_stations = 254

        st.metric("Unique Stations (Used)", f"{unique_stations}")
        st.metric("Data Period", f"{start_time.strftime('%b %d')} – {end_time.strftime('%b %d')}")
        st.metric("Total Trips", f"{total_trips:,}")
        st.metric("Avg Trips per Hour", f"{total_trips / duration_hours:.1f}")
        st.metric("Avg Trip Duration (min)", f"{avg_duration:.1f}")

        st.markdown("#### Trips per Hour of Day")
        df["hour"] = df["departure_time"].dt.hour
        hour_counts = df["hour"].value_counts().sort_index()
        st.bar_chart(hour_counts)
