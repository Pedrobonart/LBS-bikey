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
    from mypages.introduction import show_page
    show_page()
elif page == "Analysis: Heatmap":
    from mypages.heatmap import show_page
    show_page()
elif page == "Analysis: Network":
    from mypages.network import show_page
    show_page()
elif page == "Analysis: Balance":
    from mypages.balance import show_page
    show_page()
elif page == "Analysis: Trajectories":
    from pages.trajectories import show_page
    show_page()
elif page == "Analysis: Autocorrelation":
    from mypages.autocorrelation import show_page
    show_page()
elif page == "Conclusion":
    from mypages.conclusion import show_page
    show_page()

st.markdown("""---""")
st.caption("Project by Ballardini, Bonilla, Pauly and Tockner • Technical University of Vienna • 2025")
