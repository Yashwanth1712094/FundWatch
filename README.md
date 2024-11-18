# FundWatch

This application provides comprehensive details about mutual fund schemes, assisting users in making informed investment decisions. It tracks the performance of their investments, monitors wealth accumulation, and calculates gains over time, enabling efficient management of their investment portfolio.



## Installation

1.python3.10 -m venv venv
2.source venv/bin/activate
3.pip install -r requirements.txt

#Open two terminals one for frontend and another for backend apis
#Activate the virtual environments in both the terminals
  
4.python main.py     (in terminal 1)
5.streamlit run frontend/app.py    (in terminal 2)   


## Folder Strutchure

├── README.md      
├── __init__.py
├── backend                     <-  Contains the apis and functions related to backend
│   ├── __init__.py
│   ├── api.py                  <-  Python file used to maintain core logic for all apis
│   ├── database.py             <-  Python file for all database related transactions
│   ├── global_var.py           <-  Python file for maintainng the value of global variables
│   ├── routes.py               <-  Python file where api calls and routing are maintained
│   └── test1.py                <-  Python file for maintainng mock result
├── frontend                    <-  Contains the frontend logic
│   ├── __init__.py
│   ├── app.py                  <-  python file used for navigating to diferent pages
│   ├── fund_moniter_page.py    <-  python file used for presonal tracking of user wealth and investment
│   ├── investment_page.py      <-  python file used for fetching investent options
│   └── login_page.py           <-  python file used for login and registration of user
├── main.py                     <-  Main python file to run the app
└── requirements.txt            <-  Requirement file with list of libraries needed
