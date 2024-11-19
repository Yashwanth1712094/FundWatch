'''
This python file contains all the Database transactions
'''

from sqlalchemy import create_engine, Column, Integer, String, DateTime, func,Computed
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import bcrypt
from sqlalchemy import event,update
import os
import sys
from dotenv import load_dotenv
load_dotenv()

Base = declarative_base()





#This function helps in setting up of the postgres and database

def setup_postgres():
    # Enable and start the PostgreSQL service
    os.system("sudo systemctl enable postgresql")
    os.system("sudo systemctl start postgresql")
    print("PostgreSQL service started and enabled.")

    # Create a PostgreSQL user
    create_user_command = """sudo -i -u postgres psql -c "CREATE USER my_user WITH PASSWORD 'password' SUPERUSER;" """
    os.system(create_user_command)
    print("User 'my_user' created.")

    # Create a PostgreSQL database
    create_db_command = """sudo -i -u postgres psql -c "CREATE DATABASE bhive;" """
    os.system(create_db_command)
    print("Database 'bhive' created.")

    # Grant privileges to the user
    grant_privileges_command = """sudo -i -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE bhive TO my_user;" """
    os.system(grant_privileges_command)
    print("Privileges granted to 'my_user' on 'bhive' database.")

setup_postgres()



# User class keeps the track of user email and password credentials
class User(Base):
    __tablename__ = 'user_cred'

    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())




#User Fund keeps the track of the user investments and portfolio
class User_Fund(Base):

    __tablename__='user_fund'
    stock_id = Column(Integer, primary_key=True,unique=True,nullable=False)
    email = Column(String(100), nullable=False)
    scheme_code=Column(String(200), nullable=False)
    stock_name = Column(String(200),nullable=False)
    initial_stock_value=Column(Integer, unique=True, nullable=False)
    current_value=Column(Integer, nullable=False)
    quantity=Column(Integer, nullable=False)
    gain = Column(Integer, Computed('(current_value - initial_stock_value) * quantity', persisted=True))
    purchased_at = Column(DateTime, default=func.now())



#Family Fund class keeps the track of all schemes
class Family_Fund_Details(Base):
    __tablename__='family_fund_details'
    stock_id = Column(Integer, primary_key=True)
    scheme_code=Column(String(200), unique=True, nullable=False)
    stock_name = Column(String(200), nullable=False)
    curr_stock_value=Column(Integer, nullable=False)
    scheme_type=Column(String(200), nullable=False)
    mutual_fund_family=Column(String(200), nullable=False)
    last_updated=Column(DateTime, default=func.now())
# PostgreSQL database URL
DATABASE_URL = "postgresql://my_user:password@localhost:5432/bhive"

# Create the engine and session
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Create tables
Base.metadata.create_all(engine)
print("Database and tables are created!")


#This function will update the latest NAV of a scheme and add if there is any new scheme in Family_fund user
def insert_fund_family_details(scheme_Code,stock_name,curr_stock_value,scheme_type,mutual_fund_family):
    try:
        existing_scheme_code = session.query(Family_Fund_Details).filter(Family_Fund_Details.scheme_code == scheme_Code).first()
        if existing_scheme_code:
            existing_scheme_code.curr_stock_value=curr_stock_value

            session.commit()
            
            return
        else:
            new_user=Family_Fund_Details(scheme_code=scheme_Code,stock_name=stock_name,curr_stock_value=curr_stock_value,
                                         scheme_type=scheme_type,mutual_fund_family=mutual_fund_family)
            session.add(new_user)
            session.commit()

    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close

#This functon updates the NAV value as soon as it is updated in family fund table
@event.listens_for(Family_Fund_Details, 'after_update')
def update_user_table_on_family_fund_update(mapper, connection, target):
    if target.scheme_code:  # Check if 'b' has been updated
        connection.execute(
            update(User_Fund)
            .where(User_Fund.scheme_code == target.scheme_code)  # Update Table2 where 'a' matches
            .values(current_value=target.curr_stock_value)  # Set 'b' to the updated value of Table1's 'b'
        )
      



import requests
import time
from apscheduler.schedulers.background import BackgroundScheduler

#This functions runs for every 1 hour using aps scheduler and updates the family und table with latest NAV values
def preprocess():
    try:
        print("preprocess started .please wait for server")
        url= os.getenv("RAPID_API_URL")
        querystring = {"Scheme_Type":"Open"}
        headers = {
            "x-rapidapi-key": os.getenv("RAPID_API_KEY"),
            "x-rapidapi-host": os.getenv("RAPID_API_HOST")
        }
        response = requests.get(url, headers=headers, params=querystring)
        response=response.json()
        for scheme in response:
            insert_fund_family_details(str(scheme['Scheme_Code']),scheme['Scheme_Name'],
                                                scheme['Net_Asset_Value'],scheme['Scheme_Type'],
                                                scheme['Mutual_Fund_Family'])
        print("scheme id {scheme_code} already exists updted the latest value ")
    except Exception as e:
        print(response)
        print("Error in rapid api token.Either Quota completed or invald token")
        sys.exit()
preprocess()
scheduler=BackgroundScheduler()
scheduler.add_job(preprocess,'cron',minute='*/59')