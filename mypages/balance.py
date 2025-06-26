from PIL import Image
import streamlit as st
from utils.data_loaders import load_balance_data, load_time_of_day_data
import folium
from streamlit_folium import st_folium
import pandas as pd

def show_page():
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
        st.markdown("<br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
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
        st.markdown("<br>", unsafe_allow_html=True)
        st.write("""
        This interactive collection of maps provides interesting insights to different patterns in the different time windows.
        """)

        st.markdown("<br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
        st.write("""
        Based on the balance map, are there measurable correlations between stations and their number of arrivals and departures? To answer this question, global and local Moran's I were calculated based on departures minus arrivals.
        """)
        st.write("""
        Global Moran's I provides a measure of the entire dataset ranging from -1 to 1, where -1 indicates dispersion and 1 indicates full clustering. To understand how this is reflected spatially at each station, a local Moran's analysis was applied, categorizing the data into stations based on the values of their surrounding stations
        """)

    with col2:
        balance_df = load_balance_data()
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

        st_folium(balance_map, width=700, height=500)

        df_temp = load_time_of_day_data()
        time_of_day = st.selectbox("Select time of day", ["morning", "midday", "evening", "night"])

        dep_col = f"dep_{time_of_day}"
        arr_col = f"arr_{time_of_day}"
        status_col = f"status_{time_of_day}"

        temp_map = folium.Map(location=[df_temp["lat"].mean(), df_temp["lon"].mean()], zoom_start=12)

        for _, row in df_temp.iterrows():
            dep = row[dep_col]
            arr = row[arr_col]
            status = row[status_col]
            diff = dep - arr

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
            <b>Arrivals:</b> {int(arr)}
            """

            folium.CircleMarker(
                location=[row["lat"], row["lon"]],
                radius=radius,
                color=color,
                fill=True,
                fill_opacity=0.6,
                popup=folium.Popup(popup_text, max_width=300)
            ).add_to(temp_map)

        st_folium(temp_map, width=700, height=500)
        
        
        time_of_day_auto = st.selectbox("Choose time of day", ["morning", "midday", "evening", "night"])
        # Construct image path
        image_path_auto = f"data/autocorrelation_{time_of_day_auto}.png"
        # Load and show image
        image_auto = Image.open(image_path_auto)
        st.image(image_auto, caption=f"{time_of_day_auto.capitalize()} Autocorrelation Map", use_container_width=True)

    with col3:
        st.markdown("### Data Summary")
        st.metric("Most Imbalanced Station", "Dänenstr. / BOKU")
        st.metric("Total Stations", len(balance_df))
        more_departures = (balance_df["diff"] > 0).sum()
        more_arrivals = (balance_df["diff"] < 0).sum()
        st.markdown(f"**⬜ Perfectly Balanced:** **13 stations**")
        st.markdown(f"**🟩 More Departures:** **123 stations**")
        st.markdown(f"**🟦 More Arrivals:** **118 stations**")

        st.markdown("<br><br><br><br><br><br><br>", unsafe_allow_html=True)
        data_tabl = {
            "Time of Day": ["Morning", "Midday", "Evening", "Night"],
            "Amount of Trips": [3424, 5340, 6907, 4901],
            "Mean Duration (min)": [30.77, 35.23, 34.18, 28.54]
        }
        df_tabl = pd.DataFrame(data_tabl)
        st.markdown("### Summary by Time of Day")
        st.table(df_tabl)

        st.markdown("<br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
        st.write("""
        
        1. high values surrounded by high values (HH)
        2. High values surrounded by low values (HL)
        3. Low values surrounded by high values (LH)
        4. Low values surrounded by low values (LL)
        5. Cells with no significance
        """)
        st.write("""
        Values of LH and HL indicate spatial outliers, while values of HH and LL indicate clusters.
        """)

        st.write("""
        - Morning:	0.15
        - Midday:	0.12
        - Evening:	0.06
        - Night:	0.33
        	
        - Average:	0.03
        """)
