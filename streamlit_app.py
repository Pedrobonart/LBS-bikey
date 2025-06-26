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
    page_title='Vienna’s share bike system',
    page_icon=':bike:', # This is an emoji shortcode. Could be a URL too.
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
                                  "Analysis: Balance",
                                  "Analysis: Trajectories",
                                  "Analysis: Autocorrelation",
                                  "Analysis: Network",
                                  "Conclusion"])

if page == "Introduction":
    st.header("Introduction")

    # Create a 3-column layout
    col1, col2, col3 = st.columns([1.5, 2, 1.5])  # Adjust ratio as needed

    with col1:
        st.markdown("### About the Project")
        st.write("""
        With cities growing rapidly, there’s an urgent need to rethink how we move through urban spaces. Making cities less dependent on cars is a key step toward more sustainable and inclusive living. Public bikes offer a healthy, affordable, and flexible way to get around—especially for short trips or to connect with other public transport. But how well is this system working in Vienna? This project looks closely at the city’s bike-sharing system - specifically the Nextbike WienMobil system -, identifies key challenges, and explores ways to improve it using a location-based approach. There are 254 bike stations spread across the city, allowing people to rent bikes and ride them to other stations.
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
        # Centered map
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
        map_center = [48.21204, 16.37733]
        heat_map = folium.Map(location=map_center, zoom_start=11, min_zoom=10)
        HeatMap(heat_points, radius=15, blur=20, max_zoom=1, opacity=0.8, gradient={0.0: '#ffffff', 0.333:'#ffd43b', 0.6667:'#ed6d0c', 1:'#d62b2b'}).add_to(heat_map)

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
    
elif page == "Analysis: Balance":
    st.header("Origin vs. Destination Balance")
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        st.markdown("### Station Activity")
        st.write("""
        This map shows the **net balance of trips** at each station:  
        - Green markers indicate more **departures**  
        - Blue markers indicate more **arrivals**  
        - Grey markers mean **balanced traffic**
        """)
        st.write("""
        The size of each marker reflects the **magnitude of imbalance**.
        """)
        st.markdown("<br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
        st.write("""
        Now let's take a look at the different times of day.
        """)
        st.write("""
        For this part of the analysis, **4 time windows** are defined:
        - Morning: **7:00 - 11:00**
        - Midday: **11:00 - 16:00**
        - Evening: **16:00 - 20:00**
        - Night: **20:00 - 7:00**
        """)

    with col2:
        balance_df = pd.read_csv("data/station_dep_vs_arr (1).csv")
        balance_df["diff"] = balance_df["dep_count"] - balance_df["arr_count"]

        map_center = [balance_df["lat"].mean(), balance_df["lon"].mean()]
        balance_map = folium.Map(location=map_center, zoom_start=12)

        for _, row in balance_df.iterrows():
            diff = row["diff"]
            if diff > 0:
                color = "green"
            elif diff < 0:
                color = "blue"
            else:
                color = "gray"

            # Größe proportional zur Differenz (mit Mindestgröße)
            radius = max(4, min(12, abs(diff)/3))

            popup_text = f"""
            <b>{row['station']}</b><br>
            Departures: {int(row['dep_count'])}<br>
            Arrivals: {int(row['arr_count'])}<br>
            """

            folium.CircleMarker(
                location=[row["lat"], row["lon"]],
                radius=radius,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.6,
                popup=folium.Popup(popup_text, max_width=250)
            ).add_to(balance_map)

        st_folium(balance_map, width=500, height=500)

        df_temp = pd.read_csv("data/station_arr_dep_time (1).csv")
        time_of_day = st.selectbox("Select time of day", ["morning", "midday", "evening", "night"])

        # Dynamische Spaltennamen auf Basis der Auswahl
        dep_col = f"dep_{time_of_day}"
        arr_col = f"arr_{time_of_day}"
        status_col = f"status_{time_of_day}"

        # Karte vorbereiten
        temp_map = folium.Map(location=[df_temp["lat"].mean(), df_temp["lon"].mean()], zoom_start=12)

        for _, row in df_temp.iterrows():
            dep = row[dep_col]
            arr = row[arr_col]
            status = row[status_col]
            total = dep + arr
            diff = dep - arr

            # Farbe und Radius festlegen
            if status == "more_arrivals":
                color = "blue"
            elif status == "more_departures":
                color = "green"
            else:
                color = "gray"

            radius = max(4, min(12, abs(diff)/3))

            popup_text = f"""
            <b>Station:</b> {row['station']}<br>
            <b>Departures:</b> {int(dep)}<br>
            <b>Arrivals:</b> {int(arr)}<br>
            <b>Status:</b> {status}
            """

            folium.CircleMarker(
                location=[row["lat"], row["lon"]],
                radius=radius,
                color=color,
                fill=True,
                fill_opacity=0.6,
                popup=folium.Popup(popup_text, max_width=300)
            ).add_to(temp_map)

        st_folium(temp_map, width=500, height=500)


    with col3:
        st.markdown("### Data Summary")
        st.metric("Most Imbalanced Station", 
                  balance_df.loc[balance_df["diff"].abs().idxmax(), "station"])
        st.metric("Total Stations", len(balance_df))
        more_departures = (balance_df["diff"] > 0).sum()
        more_arrivals = (balance_df["diff"] < 0).sum()
        st.markdown(f"**⬜ Perfectly Balanced:** **13 stations**")
        st.markdown(f"**🟩 More Departures:** **123 stations**")
        st.markdown(f"**🟦 More Arrivals:** **118 stations**")

        st.markdown("<br><br><br>", unsafe_allow_html=True)
        data_tabl = {
            "Time of Day": ["Morning", "Midday", "Evening", "Night"],
            "# Trips": [3424, 5340, 6907, 4901],
            "Mean Duration (min)": [30.8, 35.2, 34.2, 28.5]
        }
        df_tabl = pd.DataFrame(data_tabl)
        # Show it in Streamlit
        st.markdown("### Summary by Time of Day")
        st.dataframe(df_tabl, use_container_width=True)

elif page == "Analysis: Network":
    st.header("Connectiveness of Stations")
    col1, col2, col3 = st.columns([1.5, 3, 1])

    with col1:
        st.markdown("### Networks")
        st.write("""
        This map shows how connected each station is, with the size indicating the degree of centrality
        """)
        

    with col2:
        network_df = pd.read_csv("data/network_extended.csv")

        network_df = network_df.dropna(subset=["lat", "lon"])

        map_center = [network_df["lat"].mean(), network_df["lon"].mean()]
        network_map = folium.Map(location=map_center, zoom_start=12)

        min_c = network_df["degree_centrality"].min()
        max_c = network_df["degree_centrality"].max()
        
        def scale_radius(value, min_size=0.5, max_size=15):
            if max_c == min_c:
                return min_size
            norm = (value - min_c) / (max_c - min_c)
            return min_size + norm * (max_size - min_size)
        
        for _, row in network_df.iterrows():
            centr = row["degree_centrality"]
            radius = scale_radius(centr)

            popup_text = f"""
            <b>{row['station']}</b><br>
            Degree of Centrality: {centr:.3f}<br>
            Number of Trips: {int(row['trips'])}<br>
            Number of Stations trips are going to: {int(row['connections_out'])}<br>
            Number of stations trips are coming from : {int(row['connections_in'])}
            """

            folium.CircleMarker(
                location=[row["lat"], row["lon"]],
                radius=radius,
                color="gray",
                fill=True,
                fill_color="gray",
                fill_opacity=0.6,
                popup=folium.Popup(popup_text, max_width=250)
            ).add_to(network_map)

        st_folium(network_map, width=500, height=500)

    with col3:
        st.markdown("### Data Summary")
        st.metric("Station with the most Centrality", 
                  network_df.loc[network_df["degree_centrality"].abs().idxmax(), "station"])
    

elif page == "Conclusion":
    st.header("Conclusion & Recommendations")
    st.write("""
        Based on the data, we can identify optimization potential in the network.
        For example, we propose additional stations in underserved areas.
    """)

# --- Fußzeile ---
st.markdown("""---""")
st.caption("Project by Number 4 :) • Technical University of Vienna • 2025")
