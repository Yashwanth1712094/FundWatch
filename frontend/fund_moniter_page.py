import streamlit as st
import sys
import os
import requests
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend import global_var
def show_fund_monter():
    st.text(f"current_email:{global_var.get_variable()}")
    st.title("FundMoniter Page")
    st.write("Welcome to the FundMoniter page of this multipage app!")
    st.title("Display API Data in Pretty Format")

# Fetch data from API
    data = fetch_data_from_api()
    
    if data:
        # Loop through the data (assuming it's a list of lists of dictionaries)
        for idx, data_list in enumerate(data):
            st.subheader(f"List {idx + 1}")

            # Convert each list of dictionaries to a Pandas DataFrame for better visualization
            df = pd.DataFrame(data_list)
            
            # Display as a dataframe (pretty table view)
            st.dataframe(df)
    else:
        st.write("No data available to display.")

# Function to fetch data from the API
def fetch_data_from_api():
    # Example API URL (replace with the actual API URL)
    api_url = "http://localhost:5000/My_profile"
    
    # Send the GET request to the API
    response = requests.post(api_url,data={'email':global_var.get_variable()})
    print(response.json())
    # If the response status code is OK
    if response.status_code == 200:
        return response.json()  # Return the response data as JSON (list of dictionaries)
    else:
        st.error("Error fetching data from API")
        return None


