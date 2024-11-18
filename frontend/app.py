# app.py
import streamlit as st
import fund_moniter_page
import investment_page
import login_page

st.sidebar.title("Navigation")
page = st.sidebar.radio("Choose a page", ['login_page', 'investment_page', 'fund_moniter_page'])

if page == 'login_page':
    login_page.main()
elif page == 'investment_page':
    investment_page.main()
elif page == 'fund_moniter_page':
    fund_moniter_page.main()