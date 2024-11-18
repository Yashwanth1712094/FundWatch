import streamlit as st
import sys
import requests
import os
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend import global_var
API_BASE_URL = "http://localhost:5000"  # Change to your actual API base URL
UNIQUE_FAMILY_FUNDS_URL = f"{API_BASE_URL}//Get_Fund_Houses"
DIFF_SCHEMES_URL = f"{API_BASE_URL}//Get_schemes"
INVEST_URL= f"{API_BASE_URL}//Invest"
def show_investment(selected_fund_family):
    st.text(f"current_email:{global_var.get_variable()}")
    res=requests.post(DIFF_SCHEMES_URL,data={'fund_house':selected_fund_family})
    scheme_id_list=[]
    for i in res.json()['response']:
        scheme_id_list.append(str(i['scheme_id']))
    df_schemes = pd.DataFrame(res.json()['response'])

    st.subheader("List of All Schemes")
    st.dataframe(df_schemes)
    entered_scheme_id = st.text_input("Enter Scheme ID u want to buy", None)
    if entered_scheme_id:
        ind = scheme_id_list.index(str(entered_scheme_id))
        st.write("details of the scheme selected:")
        st.json(res.json()['response'][ind])
        quantity = st.text_input("no of stocks to buy", None)
        if quantity:
            total_amount=int(quantity)*res.json()['response'][ind]['price']
            st.write(f"Amount to be paid:{total_amount}")
            res=res.json()['response'][ind]
            if st.button("submit"):
                res=requests.post(INVEST_URL,data={'email':global_var.get_variable(),"scheme_code":res['scheme_code'],'scheme_name':res['scheme_name'],
                                           'price':res['price'],'quantity':quantity
                                           })
                st.success(f"Stock bought successfully")
                st.json(res.json())
                
            else:
                st.write("please press submit to submit")
        else:
            st.write("enter quantity to procees")
    else:   
        pass
    
def main():
    if global_var.get_variable()==None:
        st.write("Login first to view schemes")
        return
    st.text(f"current_email:{global_var.get_variable()}")
    st.title("Investment Page")
    st.write("Welcome to the Investment page of this multipage app!")
    res=requests.post(UNIQUE_FAMILY_FUNDS_URL)
    list_of_family_funds=res.json()['response']
    selected_fund_family=st.radio("Select Fund Family", list_of_family_funds)
    show_investment(selected_fund_family)
    