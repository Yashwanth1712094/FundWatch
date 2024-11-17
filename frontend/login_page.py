import streamlit as st
import requests
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend import global_var
# Define the API URLs (replace with your actual endpoints)
API_BASE_URL = "http://localhost:5000"  # Change to your actual API base URL
LOGIN_URL = f"{API_BASE_URL}/Login"
REGISTER_URL = f"{API_BASE_URL}/Register"

def login_user(email, password):
    """Function to make a POST request to the /Login endpoint"""
    payload = {"email": email, "password": password}
    response = requests.post(LOGIN_URL, data=payload)
    return response

def register_user(email, password):
    """Function to make a POST request to the /Register endpoint"""
    payload = {"email": email, "password": password}
    response = requests.post(REGISTER_URL, data=payload)
    return response

def register_login(page_mode):
    """Streamlit app to manage the login and registration flow"""
    st.title("Login and Registration")

    # Get current page mode from session state
    # page_mode = st.session_state.get('page_mode', 'login')  # default to login page

    # If on login page
    if page_mode == 'login':
        st.subheader("Login")
        email = st.text_input("Email", type="default")
        password = st.text_input("Password", type="default")

        if st.button("Login"):
            if email and password:
                # Attempt to log ins
                response = login_user(email, password)
                if response.status_code == 200 and response.json()['response']=="Login successful!":
                    # Registration successful
                    st.success(f"Login successful with email:{email}")
                    global_var.set_variable(email)
                    
                    st.json(response.json())  # Optionally show response data (e.g., user details or token)
                elif response.status_code == 200 and response.json()['response']=="Invalid password!":
                    st.success("Invalid password.PLease enter valid password")
                    st.json(response.json())
                elif response.status_code == 200 and response.json()['response']=="User not found!":
                    st.success("Email Not found.Please Register by clicking on register")
                    st.json(response.json())
                else:
                    st.error("Login failed. Please try again.")
            else:
                st.error("Please enter both email and password.")

    # If on registration page
    elif page_mode == 'register':
        st.subheader("Register")
        email = st.text_input("Email", type="default", key="register_email")
        password = st.text_input("Password", type="default", key="register_password")

        if st.button("Register"):
            if email and password:
                # Attempt to register
                response = register_user(email, password)
                
                if response.status_code == 200 and response.json()['response']=="User registered successfully!":
                    # Registration successful
                    st.success("Registration successful . Please Login by clicking on login")
                    st.json(response.json())  # Optionally show response data (e.g., user details or token)
                elif response.status_code == 200 and response.json()['response']=="email already exists!":
                    st.success("Email already exists. Please Login or register with another email")
                    st.json(response.json())
                else:
                    st.error("Registration failed. Please try again.")
            else:
                st.error("Please enter both email and password.")


def main():
    st.text(f"current_email:{global_var.get_variable()}")
    page_mode=st.radio("Select Action", ["login", "register"])
    
    register_login(page_mode)