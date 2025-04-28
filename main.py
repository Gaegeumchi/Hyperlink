import streamlit as st
import streamlit.components.v1 as components



# with open("google_analytics.html", "r") as f:
#     html_code = f.read()
#     components.html(html_code, height=0)

pg = st.navigation([
    st.Page("pages/upload.py", title="Upload Center", icon="🔼"),
    st.Page("pages/download.py", title="Donwload Center", icon="🔽"),
])
pg.run()