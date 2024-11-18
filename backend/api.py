'''
This python file contains all the core logic of the python api calls
'''

from backend.database import Family_Fund_Details,User_Fund,User,session
from sqlalchemy import distinct
import bcrypt


# This function is used to login the user
def login(email, password):
    try:
        # Fetch the user by username
        user = session.query(User).filter(User.email == email).first()
        if user:
            # Compare the provided password with the stored hash
            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return "Login successful!"
                
            else:
                return "Invalid password!"
        else:
            return "User not found!"
    except Exception as e:
        return f"Error: {e}"


#This functon is used for the signup of the user
def signup(email, password):
    try:
        # Check if the user already exists
        existing_user = session.query(User).filter(User.email == email).first()
        if existing_user:
            return "email already exists!"
        
        # Hash the password
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Create a new user
        new_user = User(email=email, password=password_hash.decode('utf-8'))
        session.add(new_user)
        session.commit()
        return "User registered successfully!"
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
    

#This function is used to fetch all the fund famils from Family_Fund database
def unique_fund_family_details():
    try:
        unique_categories = session.query(distinct(Family_Fund_Details.mutual_fund_family)).all()
        fund_list=[]
        for i in unique_categories:
            fund_list.append(list(i)[0])
        return fund_list
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")


#This function is used to fetch all the schemes in selected Family_Fund from family fund database 
def get_different_schemes(family_fund):
    try:
        scheme_details=session.query(Family_Fund_Details).filter(Family_Fund_Details.mutual_fund_family == family_fund).all()
        scheme_list=[]
        for i in scheme_details:
            scheme={}
            scheme['scheme_id']=i.stock_id
            scheme['scheme_code']=i.scheme_code
            scheme['scheme_name']=i.stock_name
            scheme['price']=i.curr_stock_value
            scheme_list.append(scheme)
        return scheme_list
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")


#This function is used to select the schemes and invest in the schemes 
def invest(email,scheme_code,scheme_name,price,quantity):
    try:
        new_user=User_Fund(email=email,scheme_code=scheme_code,stock_name=scheme_name, initial_stock_value=price,current_value=price,
                        quantity=quantity)
        session.add(new_user)
        session.commit()
        return f"successfully invested {price*quantity} in {scheme_name}"
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")


# This function is used or the tracting of a user portfolio
def my_profle(email):
    try:
        profile_details=session.query(User_Fund).filter(User_Fund.email == email).all()
        scheme_list=[]
        total_investment=0
        current_investment_value=0
        for i in profile_details:
            scheme={}
            scheme['scheme_id']=i.stock_id
            scheme['scheme_code']=i.scheme_code
            scheme['scheme_name']=i.stock_name
            scheme['initial_price']=i.initial_stock_value
            scheme['quantity']=i.quantity
            scheme['current_value']=i.current_value
            scheme['gain']=i.gain
            total_investment+=i.initial_stock_value*i.quantity
            current_investment_value+=i.current_value*i.quantity
            scheme_list.append(scheme)
        total_gain=current_investment_value-total_investment
        
        return scheme_list,total_gain
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")

