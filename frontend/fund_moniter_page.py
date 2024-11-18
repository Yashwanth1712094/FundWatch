import streamlit as st
import sys
import requests
import os
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend import global_var
API_BASE_URL = "http://localhost:5000"  # Change to your actual API base URL
MY_PROFILE_URL = f"{API_BASE_URL}/My_profile"




    
def main():
    if global_var.get_variable()==None:
        st.write("Login first to view schemes")
        return
    st.text(f"current_email:{global_var.get_variable()}")
    st.title("Fund Moniter Page")
    st.write("Welcome to the Fund Moniter page of this multipage app!")
    res=requests.post(MY_PROFILE_URL,data={'email':global_var.get_variable()})
    df_schemes = pd.DataFrame(res.json()['response1'])
    # df_schemes=st.dataframe(df_schemes,width=3000)
    st.subheader("List of All Schemes")
    st.dataframe(df_schemes)
    st.write(f"total gain :{res.json()['response2']} ")