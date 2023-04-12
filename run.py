import streamlit as st
import pandas as pd
from src.scifinder import get_data
from src.eln import update_data

# st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)

# st.markdown("""
# <nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: #3498DB;">
#   <a class="navbar-brand" href="https://youtube.com/dataprofessor" target="_blank">Data Professor</a>
#   <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
#     <span class="navbar-toggler-icon"></span>
#   </button>
#   <div class="collapse navbar-collapse" id="navbarNav">
#     <ul class="navbar-nav">
#       <li class="nav-item active">
#         <a class="nav-link disabled" href="#">Home <span class="sr-only">(current)</span></a>
#       </li>
#       <li class="nav-item">
#         <a class="nav-link" href="https://youtube.com/dataprofessor" target="_blank">YouTube</a>
#       </li>
#       <li class="nav-item">
#         <a class="nav-link" href="https://twitter.com/thedataprof" target="_blank">Twitter</a>
#       </li>
#     </ul>
#   </div>
# </nav>
# """, unsafe_allow_html=True)

st.markdown("""
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
      <a class="navbar-brand" href="{{url_for('index')}}">
        <img src="{{ url_for('static', filename='catsci.svg') }}" alt="" width="100" height="10" class="d-inline-block align-text-top">
        </a>
    </div>
  </nav>
""", unsafe_allow_html= True)

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
api_input = st.radio("Select an API", ('PubChem', 'SciFinder'))
# scifinder_check = st.radio('SciFinder')

if st.button('Search'):
    # add try except instead if uploaded_files
    query_params = st.experimental_get_query_params()
    eid = query_params['__eid'][0]
    try:
        filename = uploaded_file.name
        if ".xlsx" in filename:
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file)
        
        if api_input == "PubChem":
            df = get_data(df= df, source= "pubchem")
        
        if api_input == "SciFinder":
            df = get_data(df= df, source= "scifinder")

        # st.dataframe(df)
        st.info('Uplaoding data to ELN')
        var = update_data(dataframe= df, eid = eid)
        if var == 'true':
            st.success('Data Uplaoded Successfully')
        else:
            st.error('data Was not uplaoded')

        

    except Exception as e:
        st.error(e)
    
