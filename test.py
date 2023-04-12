import streamlit as st
from streamlit.hashing import _CodeHasher
import SessionState

def get_eid_from_url(url):
    parsed_url = urlparse(url)
    eid = parse_qs(parsed_url.query).get('__eid', None)
    if eid is not None and len(eid) > 0:
        return eid[0]
    else:
        return None

# Create a new SessionState object
session_state = SessionState.get(url='')

# Create a button in the Streamlit app
if st.button('Get URL'):
    # Get the current URL of the page
    session_state.url = st.experimental_get_query_params()['url'][0]
    st.write("Current URL:", session_state.url)

    # Extract the eid parameter from the URL
    eid = get_eid_from_url(session_state.url)
    if eid is not None:
        st.write("eid:", eid)
    else:
        st.write("eid not found in URL.")
