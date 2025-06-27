from PIL import Image
import streamlit as st
import pandas as pd

def show_page():
    st.header("Capacity Analysis")
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        st.markdown("### Capacity Autocorrelation")
        st.write("""
            Each bike station has a certain capacity for the number of bikes. 
            The average occupancy percentage per station was calculated for the entire timeframe. 
            Global and local Moran's I were then calculated to determine if there is a spatial 
            relationship between stations with high and low capacities.
        """)
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.write("""
        High-high clusters can be observed in the first 1st and 4th district, while there are low-low clusters
        f.ex. between the Ring and the Gürtel, giving further interesting insights to the system.
        """)

    with col2:
        image = Image.open("data/autocorrelation_capacity.png")
        st.image(image, caption="Autocorrelation value per station", use_container_width=True)

    with col3:
        st.markdown("### Explanation")
        st.write("""
        Global Moran's I provides a measure of the entire dataset ranging from -1 to 1, 
        where -1 indicates dispersion and 1 indicates full clustering. 
        To understand how this is reflected spatially at each station, 
        a local Moran's analysis was applied, categorizing the data 
        into stations based on the values of their surrounding stations.

            1. High values surrounded by high values (HH)
            2. High values surrounded by low values (HL)
            3. Low values surrounded by high values (LH)
            4. Low values surrounded by low values (LL)
            5. Cells with no significance

        Values of LH and HL indicate spatial outliers, while values of HH and LL indicate clusters.
        """)
        
        data_tabl = {
            "Label": ["HH", "LL", "HL", "LH", "Non-Significant"],
            "Stations": [14, 13, 4, 2, 161]
        }
        df_tabl = pd.DataFrame(data_tabl)
        st.markdown("### Global Moran's I: 0.13")
        st.table(df_tabl)
