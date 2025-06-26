import streamlit as st
import pandas as pd

def show_page():
    st.header("Autocorrelation Analysis")
    st.write("Autocorrelation analysis page placeholder. Add your autocorrelation visualizations and analysis here.")
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        st.markdown("### Capacity Autocorrelation")
        st.write("""
        Global Moran's I provides a measure of the entire dataset ranging from -1 to 1, 
        where -1 indicates dispersion and 1 indicates full clustering. 
        To understand how this is reflected spatially at each station, 
        a local Moran's analysis was applied, categorizing the data 
        into stations based on the values of their surrounding stations.

            1. high values surrounded by high values (HH)
            2. High values surrounded by low values (HL)
            3. Low values surrounded by high values (LH)
            4. Low values surrounded by low values (LL)
            5. Cells with no significance

        Values of LH and HL indicate spatial outliers, while values of HH and LL indicate clusters.
        """)

    with col2:
        # You can add visualizations or more content here for col2
        pass

    with col3:
        st.markdown("### Explenation")
        st.write("""
        Each bike station has a certain capacity for the number of bikes. 
        The average occupancy percentage per station was calculated for the entire timeframe. 
        Global and local Moran's I were then calculated to determine if there is a spatial relationship 
        between stations with high and low capacities.
        """)
        
        data_tabl = {
            "Label": ["Non-Significant", "HH", "Evening", "Night"],
            "Amount of Trips": [3424, 5340, 6907, 4901]
        }
        df_tabl = pd.DataFrame(data_tabl)
        st.markdown("### Summary by Time of Day")
        st.table(df_tabl)
