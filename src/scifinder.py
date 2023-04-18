from src.exception import CustomException
from src.logger import logging
import requests
import time
import streamlit as st
import pandas as pd

from src.constant.scifinder_constant import BASE_URL

from src.constant.pubchem import PUBCHEM_URL, PROPERTY

# BASE_URL = f"https://commonchemistry.cas.org/api/detail?cas_rn="

def pubchem(cas_no):
    st.write('Pubchem')
    url = url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{cas_no}/property/CanonicalSMILES,InChi/JSON"

    response = requests.get(url)
    if response.status_code == 200:
        try:
            logging.info('Extracting Data using GET request Started')
            # for pubchecm
            response_data = response.json()['PropertyTable']['Properties'][0]
            canonical_smile = response_data['CanonicalSMILES']
            inchi = response_data['InChI'].replace('InChI=1S/', '')
            
            return {'Smile': canonical_smile,
                    'InChi': inchi}
        except (KeyError, IndexError):
            logging.error('Exception Occurred')
            return None

    time.sleep(0.25)

def scifinder(cas_no):
    st.write('Scifinder')
    url = BASE_URL + cas_no

    response = requests.get(url)
    if response.status_code == 200:
        try:
            logging.info('Extracting Data using GET request Started')
            # for scifinder
            response_data = response.json()
            canonical_smile = response_data['canonicalSmile']
            inchi = response_data['inchi'].replace('InChI=1S/', '')
            
            return {'Smile': canonical_smile,
                    'InChi': inchi}
        except (KeyError, IndexError):
            logging.error('Exception Occurred')
            return None

    time.sleep(0.25)


def get_info(source, cas_no, url = BASE_URL):
    if source == "scifinder":
        d = scifinder(cas_no= cas_no)
    else:
        d = pubchem(cas_no= cas_no)

    return d

def get_data(df, source):
    df["SMILES"] = ""
    df["InChI"] = ""
    progress_bar = st.progress(0)
    status_text = st.empty()
    for i, cas_number in df["CAS Number"].items():
        if pd.isna(cas_number):
            df.at[i, "SMILES"] = ""
            df.at[i , "InChI"] = ""
        else:
            result = get_info(source, cas_number)
            if result is not None:
                smile = result['Smile']
                inchi = result['InChi']
                df.at[i, "SMILES"] = smile
                df.at[i, "InChI"] = inchi
            else:
                df.at[i, "SMILES"] = ""
                df.at[i, "InChI"] = ""
        progress = (i + 1) / len(df)
        progress_bar.progress(progress)
        status_text.text(f"{int(progress*100)}% Complete")
    return df


def convert_df(df):
    return df.to_csv(index = False).encode('utf-8')

