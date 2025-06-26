import streamlit as st

def show_page():
    st.title("Conclusion")
    st.markdown("""
    ### 🚲 Key Takeaways from Our Analysis

    - In total, Vienna's Bike-Sharing performs well and is well-embedded in the infrastructure system and the allday life. However, there is still room for improvement. 
    
    - **Monocentric Usage**: Vienna’s bike-sharing is heavily centered around the inner districts (e.g., Mariahilf, Neubau), with the outer districts significantly underserved.

    - **Infrastructure Gaps**: Residential areas like Meidling and Liesing show demand (e.g., commuting flows) but lack stations — suggesting potential for expansion, especially near U-Bahn lines (U1, U3, U6).

    - **Imbalance Issues**: Stations in the center are often empty in the morning and overcrowded at night, indicating a need for smarter, time-sensitive rebalancing strategies.

    - **Land Use & Equity**: Industrial/commercial zones (e.g., Stadlau, Inzersdorf) are almost absent from trip data — a missed opportunity for modal shift via targeted infrastructure and employer partnerships.

    - **Beyond Commuting**: Midday and night trips reflect leisure usage in central districts. Infrastructure like lighting and better visibility near nightlife hubs (e.g., Naschmarkt) could boost this further.

    - **Capacity Misalignment**: Some stations (e.g., Gußhausstraße) are constantly overfull. Modular docks or pop-up stations during peak times could improve capacity and user experience.
    """)
