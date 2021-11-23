from CAS_Searcher import CAS_Searcher
import streamlit as st
import streamlit_analytics
# maybe have to run in terminal:
# streamlit run c:\Users\James\CAS_Searcher_App.py


# search_term = "66728-98-1"
# search_term = "497-23-4" # furanone test
#search_term = "12135-22-7" # Pd/C
#search_term = "74-88-4" # iodomethane 
#search_term = "45-125-15478" #Not valid CAS
#search_term = "22122-36-7"
#search_term = "100-52-7" # benzaldehyde 
# search_term = "51673-83-7" # Building block explorer
#CAS_Searcher(search_term)   


st.set_page_config(layout="wide")

st.write("""# CAS Searcher""")

with st.form(key='searchform'):
    nav1,nav2 = st.columns([1,1])

    with nav1:
        search_term = st.text_input("Enter CAS Number  eg 497-23-4", help = "eg 497-23-4", type = "default")

    with nav2:
        st.text("Search")
        submit_search = st.form_submit_button(label='Search')

col1, col2 = st.columns([2,1])

streamlit_analytics.start_tracking()
with col1:
    if submit_search:

        results = CAS_Searcher(search_term)

streamlit_analytics.stop_tracking()