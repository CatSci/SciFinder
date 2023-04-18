from src.constant.eln_constant import API_BASE_URL
import os
from dotenv import load_dotenv
import requests
from flask import request
import json
import pandas as pd
import numpy as np
import streamlit as st

from src.exception import CustomException
import sys


# load_dotenv(".env")
# API_KEY = os.getenv("API_KEY")

# API_KEY = st.secrets["API_KEY"]
# st.write(API_KEY)



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


def update_data(dataframe, eid, api_key):

    url = API_BASE_URL + f'{eid}?value=display'
    headers = {
        'x-api-key': api_key
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
        'x-api-key': api_key
    }

    
    try:
        patch_response = requests.patch(patch_url, json=payload, headers=patch_headers)
    except Exception as e:
        raise CustomException(e, sys)

    if patch_response.ok:
        return 'true'
    else:
        return f"Error adding data: {patch_response.status_code}"