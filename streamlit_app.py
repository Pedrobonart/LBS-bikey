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
    from pages.introduction import show_page
    show_page()
elif page == "Analysis: Heatmap":
    from pages.heatmap import show_page
    show_page()
elif page == "Analysis: Network":
    from pages.network import show_page
    show_page()
elif page == "Analysis: Balance":
    from pages.balance import show_page
    show_page()
elif page == "Analysis: Trajectories":
    from pages.trajectories import show_page
    show_page()
elif page == "Analysis: Autocorrelation":
    from pages.autocorrelation import show_page
    show_page()
elif page == "Conclusion":
    from pages.conclusion import show_page
    show_page()

st.markdown("""---""")
st.caption("Project by Number 4 :) • Technical University of Vienna • 2025")
