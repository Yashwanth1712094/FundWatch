import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend import global_var


def show_investment():
    st.text(f"current_email:{global_var.get_variable()}")
    st.title("Investment Page")
    st.write("Welcome to the Investment page of this multipage app!")