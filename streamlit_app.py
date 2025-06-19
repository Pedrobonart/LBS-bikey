import streamlit as st
import pandas as pd
import geopandas as gpd
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
page = st.sidebar.radio("Go to", ["Introduction", "Statistics", "Analysis", "Conclusion"])

if page == "Introduction":
    st.header("Introduction")

    # Create a 3-column layout
    col1, col2, col3 = st.columns([2, 3, 2])  # Adjust ratio as needed

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
        st_folium(bike_map, width=600, height=500)

    with col3:
        st.markdown("### More Info")
        st.write("""
        - Source: [WienMobil Rad](https://www.wien.gv.at/english/transportation/bike/)
        - Data: scraped from the Nextbike API.
        """)
        st.image("https://upload.wikimedia.org/wikipedia/commons/4/45/Nextbike_Bike-sharing_Bicycle_in_Berlin.jpg", caption="Example of a Nextbike bicycle", use_container_width=True)


elif page == "Analysis":
    st.header("In-depth Analysis")
    st.write("Visualizations like maps, usage heatmaps, movement flows etc.")
    import json
    import branca.colormap as cm

    geojson_path = 'data/agg_dur_traj (1).geojson'

    # Load the GeoJSON manually
    with open(geojson_path, "r", encoding="utf-8") as f:
        geojson_data = json.load(f)

    # Determine min/max for color scale
    durations = [feat["properties"]["avg_duration_min"] for feat in geojson_data["features"]]
    min_dur = min(durations)
    max_dur = max(durations)

    colormap = cm.linear.YlOrRd_09.scale(min_dur, max_dur)
    colormap.caption = "Average Trip Duration (min)"

    # Create map centered on mean origin
    origins = [(f["properties"]["origin_lat"], f["properties"]["origin_lon"]) for f in geojson_data["features"]]
    avg_lat = sum([lat for lat, _ in origins]) / len(origins)
    avg_lon = sum([lon for _, lon in origins]) / len(origins)

    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=12)

    # Draw lines
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
            locations=[(lat, lon) for lon, lat in coords],  # Convert to [lat, lon]
            color=color,
            weight=1 + count * 1.5,
            opacity=0.7,
            popup=folium.Popup(popup_text, max_width=300)
        ).add_to(m)

    colormap.add_to(m)
    st_folium(m, width=800, height=600)

elif page == "Conclusion":
    st.header("Conclusion & Recommendations")
    st.write("""
        Based on the data, we can identify optimization potential in the network.
        For example, we propose additional stations in underserved areas.
    """)

# --- Fußzeile ---
st.markdown("""---""")
st.caption("Project by [Your Name] • University XYZ • 2025")
