import streamlit as st

def check_limit():
    if "uses" not in st.session_state:
        st.session_state.uses = 0

    if st.session_state.uses >= 3:
        return False

    st.session_state.uses += 1
    return True