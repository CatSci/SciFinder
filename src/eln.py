from src.constant.eln_constant import API_BASE_URL
import os
from dotenv import load_dotenv
import requests
from flask import request
import json
import pandas as pd
import numpy as np
import streamlit as st
from urllib.parse  import urlparse, parse_qs
import requests


from streamlit_javascript import st_javascript

url = st_javascript("await fetch('').then(r => window.parent.location.href)")
st.write(url)

# Parse the URL to extract the query string
parsed_url = urlparse(url)

# Parse the query string to extract the value of the "eid" parameter
eid = parse_qs(parsed_url.query).get('__eid', None)

# Print the value of the "eid" parameter
if eid is not None and len(eid) > 0:
    # print("eid:", eid[0])
    st.write(eid)
else:
    st.write("eid not found in URL.")


# load_dotenv(".env")
# API_KEY = os.getenv("API_KEY")
# API_KEY = os.getenv("API_KEY")
API_KEY = st.secrets["API_KEY"]


def get_col_id(response):
    content = 'Row Not Found'
    column_definitions = None
    included = response.json().get('included')
    if included:
        for item in included:
            if item.get('type') == 'columnDefinitions':
                column_definitions = item.get('attributes')['columns']
                break
    
    column_ids = {}
    for i in column_definitions:
        column_ids[i['title']] = i['key']
    
    return content, column_ids


def update_data(dataframe):
    eid = 'grid:13cce184-65a8-4153-9620-5aafbc9c2511'

    url = API_BASE_URL + f'{eid}?value=display'
    headers = {
        'x-api-key': API_KEY
    }
    response = requests.get(url, headers=headers)

    content, column_ids = get_col_id(response= response)

    data = []
    for row_idx in range(dataframe.shape[0]):
        cell_data = []
        for col_idx, col_ids in enumerate(column_ids):
            value = dataframe.iloc[row_idx, col_idx]
            if pd.isna(value):
                # Handle NaN and infinity values
                cell_data.append({
                    'key': column_ids[col_ids],
                    'content': None  # Set to null if value is not valid JSON
                })
            else:
                cell_data.append({
                    'key': column_ids[col_ids],
                    'content': {
                        'value': dataframe.iloc[row_idx, col_idx]
                    }
                })
        
        data.append({
            'type': 'adtRow',
            'attributes': {
                'action': 'create',
                'cells': cell_data        
            }
        })

    payload = {"data": data}

    patch_url = API_BASE_URL +  f'{eid}?force=true&value=display'
    patch_headers = {
        'Content-Type': 'application/vnd.api+json',
        'x-api-key': API_KEY
    }


    patch_response = requests.patch(patch_url, json=payload, headers=patch_headers)
    if patch_response.ok:
        return 'true'
    else:
        return f"Error adding data: {patch_response.status_code}"