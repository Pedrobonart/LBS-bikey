import streamlit as st
from utils.data_loaders import load_network_data
import folium
from streamlit_folium import st_folium
import pandas as pd

def show_page():
    st.header("Connectiveness of Stations")
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        st.markdown("### Networks")
        st.write("""
        This map shows how connected each station is, with the dot size indicating the degree of centrality. 
        Clicking on a dot shows the number of stations connected to that station in both directions.
        """)

    with col2:
        network_df = load_network_data()
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

        st_folium(network_map, width=700, height=500)

    with col3:
        st.markdown("### Summary")
        st.markdown("<br><br><br><br>", unsafe_allow_html=True)
        st.metric("Station with the most Centrality", 
                  "Karlsplatz")
        st. write("""
        ...followed by Museumsquartier, Praterstern and Hauptbahnhof (Central station).
        """)
