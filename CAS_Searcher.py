
from Sigma_Aldrich import Sigma_Aldrich
from Fluorochem import Fluorochem 
from Enamine import Enamine
import streamlit as st


def CAS_Searcher(search_term):
    
    fluorochem = Fluorochem()
    fluorochem.search(search_term)
    a = fluorochem.get_results()
    for i in a:
        # print(i)
        st.write(f"""  * {i}""")
        
    enamine = Enamine()
    enamine.search(search_term)
    b = enamine.get_results()
    for i in b:
        # print(i)
        st.write(f"""  * {i}""")
    
    sigma_aldrich = Sigma_Aldrich()
    sigma_aldrich.search(search_term)
    c = sigma_aldrich.get_results()
    for i in c:
        # print(i)
        st.write(f"""  * {i}""")



#search_term = "66728-98-1"
#search_term = "497-23-4" # furanone test
#search_term = "12135-22-7" # gives two catalogue results
#search_term = "74-88-4" # iodomethane gives no results  
       
#CAS_Searcher(search_term)
