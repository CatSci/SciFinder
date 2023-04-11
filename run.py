import streamlit as st
import pandas as pd
from src.test import get_data, convert_df

st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #ed9439;
    color:#0f1b2a;
    border:None;
}
div.stButton > button:first-child:focus {
    background-color: #ed9439;
    color:#0f1b2a;
    border:None;
}
</style>""", unsafe_allow_html=True)

st.title("CAS Number to InChI Converter")
st.info('Please make sure you cas value column name is **CAS Number**')

uploaded_file = st.file_uploader("Choose a file")

if st.button('Search'):
    # add try except instead if uploaded_files
    try:
        filename = uploaded_file.name
        if ".xlsx" in filename:
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file)
        
        df = get_data(df= df)

        st.write(df)
        # if not df.empty:
        #     if st.button('Upload Data'):
        #         st.write('hi')
        #         st.stop()
        

    except Exception as e:
        st.error('File not uplaoded or correct file not uplaoded')
    
