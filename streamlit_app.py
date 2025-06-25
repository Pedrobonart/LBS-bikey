import streamlit as st
import pandas as pd
import geopandas as gpd
import math
from pathlib import Path
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='GDP dashboard',
    page_icon=':earth_americas:', # This is an emoji shortcode. Could be a URL too.
    layout="wide"
)

@st.cache_data
def get_stations_data():
    DATA_FILENAME = Path(__file__).parent / 'data/bike_tracking_stations.csv'
    return pd.read_csv(DATA_FILENAME)

@st.cache_data
def load_bike_trips():
    DATA_FILENAME = Path(__file__).parent / "data/bike_journeys_noOutliers.csv"
    return pd.read_csv(DATA_FILENAME)

@st.cache_data
def load_geojson(path):
    return gpd.read_file(path)

# load & filter data
stations_df = get_stations_data()
stations_df = stations_df[~stations_df["place_name"].str.startswith("BIKE")]

#Header
with st.container():
    st.markdown(
        """
        <div style="background-color:#f0f2f6; padding: 20px; border-radius: 10px; margin-bottom: 20px">
            <h1 style="color:#2C3E50;">🚲 Vienna Bike Sharing Dashboard</h1>
            <h4 style="color:#7f8c8d;">An interactive analysis of the WienMobil Rad system</h4>
        </div>
        """,
        unsafe_allow_html=True
    )

# --- Sidebar Navigation ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Introduction", 
                                  "Analysis: Heatmap",
                                  "Analysis: Trajectories",
                                  "Analysis: Balance",
                                  "Analysis: Capacity",
                                  "Analysis: Temporal",
                                  "Analysis: Network",
                                  "Conclusion"])

if page == "Introduction":
    st.header("Introduction")

    # Create a 3-column layout
    col1, col2, col3 = st.columns([1.5, 2, 1.5])  # Adjust ratio as needed

    with col1:
        st.markdown("### About the Project")
        st.write("""
        This project is about rental bikes in Vienna, specifically the Nextbike WienMobil system.  
        There are 254 bike stations spread across the city, allowing people to rent bikes and ride them to other stations.
        """)

        st.markdown("### Data Overview")
        st.write("""
        The map shows the current locations of all bike stations in Vienna.  
        Each marker represents one station. Clicking on it reveals the station name.
        """)

        st.markdown("### Sources")
        st.write("""
        - Source: [WienMobil Rad](https://www.wien.gv.at/english/transportation/bike/)
        - Data: scraped from the Nextbike API.
        """)

    with col2:
        # Centered map
        map_center = [stations_df["lat"].mean(), stations_df["long"].mean()]
        bike_map = folium.Map(location=map_center, zoom_start=13)
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

        # Parse Zeitspalten
        df["departure_time"] = pd.to_datetime(df["departure_time"])
        df["arrival_time"] = pd.to_datetime(df["arrival_time"])

        # Wichtige Metriken
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

        # Histogram der Startzeiten
        st.markdown("#### Trips per Hour of Day")
        df["hour"] = df["departure_time"].dt.hour
        hour_counts = df["hour"].value_counts().sort_index()

        st.bar_chart(hour_counts)

elif page == "Analysis: Heatmap":
    st.header("Heatmap")
    col1, col2, col3 = st.columns([1.5, 3, 1])  # Adjust ratio as needed

    with col1:
        st.markdown("### About the Project")
        st.write("""
        This project is about rental bikes in Vienna.... THIS IS A TEMPLATE SECTION!!! 
        """)

    with col2:
        df = load_bike_trips()

        # Extrahiere Koordinaten von Start- und Zielpunkten
        origins = df[["origin_lat", "origin_lon"]].copy()
        destinations = df[["destination_lat", "destination_lon"]].copy()
        origins.columns = ["lat", "lon"]
        destinations.columns = ["lat", "lon"]

        # Kombiniere beides
        all_points = pd.concat([origins, destinations], ignore_index=True)

        # Gruppiere und zähle
        heat_data = all_points.groupby(["lat", "lon"]).size().reset_index(name="count")
        heat_points = heat_data[["lat", "lon", "count"]].values.tolist()

        # Heatmap erzeugen
        map_center = [df["origin_lat"].mean(), df["origin_lon"].mean()]
        heat_map = folium.Map(location=map_center, zoom_start=8)
        HeatMap(heat_points, radius=15, blur=20, max_zoom=8).add_to(heat_map)

        # In Streamlit anzeigen
        st_folium(heat_map, width=500, height=500)

    with col3:
        st.markdown("### More Info")
        st.write("""
        sources, images and stuff
        """)


elif page == "Analysis: Trajectories":
    st.header("In-depth Analysis")

    # Define a three-column layout
    col1, col2, col3 = st.columns([1.5, 3, 1])  # Adjust proportions as needed

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
        import json
        import branca.colormap as cm

        geojson_path = 'data/agg_dur_traj (1).geojson'

        with open(geojson_path, "r", encoding="utf-8") as f:
            geojson_data = json.load(f)

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
                locations=[(lat, lon) for lon, lat in coords],  # Switch lon/lat to lat/lon
                color=color,
                weight=0.7 + count * 0.8,
                opacity=0.7,
                popup=folium.Popup(popup_text, max_width=300)
            ).add_to(m)

        colormap.add_to(m)
        st_folium(m, width=500, height=500)

    with col3:
        st.markdown("### Notes")
        st.write("""
        This dataset only includes trips recorded during **nighttime hours** (e.g., 10 PM–6 AM).  
        It has been **pre-aggregated** by origin/destination coordinates.
        """)
    

elif page == "Conclusion":
    st.header("Conclusion & Recommendations")
    st.write("""
        Based on the data, we can identify optimization potential in the network.
        For example, we propose additional stations in underserved areas.
    """)

# --- Fußzeile ---
st.markdown("""---""")
st.caption("Project by Number 4 :) • Technical University of Vienna • 2025")
