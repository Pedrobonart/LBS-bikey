import streamlit as st
import pandas as pd
import geopandas as gpd
import math
from pathlib import Path
import folium
from streamlit_folium import st_folium
import xml.etree.ElementTree as ET
from matplotlib.colors import to_hex


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

@st.cache_data
def parse_sld_styles(sld_path):
    tree = ET.parse(sld_path)
    root = tree.getroot()
    ns = {'sld': 'http://www.opengis.net/sld',
          'ogc': 'http://www.opengis.net/ogc',
          'se': 'http://www.opengis.net/se'}

    styles = {}
    for rule in root.findall(".//sld:Rule", ns):
        label = rule.find("sld:Name", ns).text
        css_param = rule.find(".//sld:CssParameter[@name='fill']", ns)
        if css_param is not None:
            styles[label] = css_param.text
    return styles

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
    st.write("This map shows the current locations of all bike stations in Vienna.")
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


elif page == "Statistics":
    st.header("System Statistics")
    st.write("Here you can show basic KPIs or charts.")

elif page == "Analysis":
    st.header("In-depth Analysis")
    st.write("Visualizations like maps, usage heatmaps, movement flows etc.")
st.title("GeoJSON Viewer with SLD Styling")

    geojson_path = "data/agg_dur_traj (1).geojson"
    sld_path = "data/test1.sld"

    gdf = load_geojson(geojson_path)
    sld_styles = parse_sld_styles(sld_path)

    column = st.selectbox("Choose the attribute for styling:", gdf.columns)

    center = [gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()]
    m = folium.Map(location=center, zoom_start=12)

    folium.GeoJson(
        gdf.to_json(),
        name="Styled Layer",
        style_function=style_function_factory(column, sld_styles)
    ).add_to(m)

    folium.LayerControl().add_to(m)
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
