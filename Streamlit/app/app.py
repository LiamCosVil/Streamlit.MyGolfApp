import streamlit as st

st.set_page_config(layout="wide")
st.markdown(" <style> div[class^='css-1544g2n'] { padding-top: 1rem; } </style> ", unsafe_allow_html=True)
#st.markdown(" <style> div[class^='block-container'] { padding-top: 1rem; } </style> ", unsafe_allow_html=True)

pg = st.navigation([
    st.Page("Home.py", title="Home"),
    st.Page("Streamlit\app\SG\ViewSG.py", title="ViewSG"),
    st.Page("AddRound\AddRound.py", title="AddRound"),
    st.Page("AddRound\AddRoundTest.py", title="AddRoundTest"),
    st.Page("Stats\ViewStats.py", title="ViewStats"),
])
pg.run()



# streamlit run app.py
