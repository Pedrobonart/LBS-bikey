import streamlit as st

st.set_page_config(
    page_title='Vienna’s share bike system',
    page_icon=':bike:',
    layout="wide"
)

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", [
    "Introduction",
    "Analysis: Heatmap",
    "Analysis: Network",
    "Analysis: Balance",
    "Analysis: Trajectories",
    "Analysis: Autocorrelation",
    "Conclusion"
])

if page == "Introduction":
    from last_try.introduction import show_page
    show_page()
elif page == "Analysis: Heatmap":
    from last_try.heatmap import show_page
    show_page()
elif page == "Analysis: Network":
    from last_try.network import show_page
    show_page()
elif page == "Analysis: Balance":
    from last_try.balance import show_page
    show_page()
elif page == "Analysis: Trajectories":
    from last_try.trajectories import show_page
    show_page()
elif page == "Analysis: Autocorrelation":
    from last_try.autocorrelation import show_page
    show_page()
elif page == "Conclusion":
    from last_try.conclusion import show_page
    show_page()

st.markdown("""---""")
st.caption("Project by Ballardini, Bonilla, Pauly and Tockner • Technical University of Vienna • 2025")
