import streamlit as st
import pandas as pd
from src.scifinder import get_data
from src.eln import update_data


# hide streamlit style
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)
# background-color: #ed9439;
st.markdown("""
<style>
.navbar {
  height: 80px;
  background-color: #ed9439;
  color: #ed9439;
}
.navbar-brand{
    font-size: 40px;
    margin-left:40px;
}
</style>""", unsafe_allow_html= True)


st.markdown("""
<nav class="navbar fixed-top navbar-expand-lg navbar-dark">
  <a class="navbar-brand" href="#" target="_blank">CatSci</a>
  

</nav>
""", unsafe_allow_html=True)


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

    

uploaded_file = st.file_uploader("Choose a file", type = ['csv', 'xlsx'])
api_input = st.radio("Select an API", ('PubChem', 'SciFinder'))

api_key = st.text_input('API KEY', placeholder= 'Enter your API Key', type= 'password', value= "NvPkEXLMW96UwVjsF+dDAjs8CROAtlXFG9dc9o38HTTZ/6dTIrV1sWELAa0vRvVqHHawTg==")

# scifinder_check = st.radio('SciFinder')

if st.button('Search'):
    # add try except instead if uploaded_files
    query_params = st.experimental_get_query_params()
    if query_params:
        eid = query_params['__eid'][0]
    else:
        eid = "grid:453a6a3d-0660-4524-aee5-e3f4a98446ab"     # sam
        # eid = "grid:3099e22d-e8cf-41c8-aee6-beb73c68adeb"     # atul
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
        st.info('Uploading data to ELN')
        try:
            var = update_data(dataframe=df, eid=eid, api_key=api_key)
            if var == True:
                st.success('Data Uploaded Successfully')
            else:
                st.error('Data was not uploaded')
                st.error(var)
        except Exception as e:
            st.error(f"An error occurred while uploading data: {str(e)}")    

    except Exception as e:
        st.error(e)
    



# https://catsci-sandbox.signalsnotebook.perkinelmercloud.eu/api/rest/v1.0/adt/grid%3A453a6a3d-0660-4524-aee5-e3f4a98446ab?value=display
# https://catsci-sandbox.signalsnotebook.perkinelmercloud.eu/api/rest/v1.0/adt/grid%3A453a6a3d-0660-4524-aee5-e3f4a98446ab?value=display