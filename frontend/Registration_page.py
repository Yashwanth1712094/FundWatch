import streamlit as st
import requests

email=""
API_URL_Login = "http://localhost:5000/Login"
API_URL_Register = "http://localhost:5000/Register"



    

def show_Register():
    st.title("Registration Form")

    # Input fields for email and password
    email = st.text_input("Email_Reg", type="default")
    password = st.text_input("Password_reg", type="default")

    if st.button("Submit"):
        if email and password:
            # Call the submit_data function to send the request
            response = submit_data_register(email, password)

            if "error" in response:
                st.error(response["error"])  # Show error message if something went wrong
            else:
                st.success("Data submitted successfully!")
                st.json(response)  # Optionally display the response from the API
        else:
            st.error("Please enter both email and password.")
        
def submit_data_register(email, password):
    """Send email and password as a POST request to the API"""
    payload = {"email": email, "password": password}
    response = requests.post(API_URL_Register, data=payload)
    
    if response.status_code == 200:
        return response.json()  # Return response data if successful
    else:
        return {"error": "Failed to submit data"}
    