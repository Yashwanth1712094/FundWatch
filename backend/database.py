from sqlalchemy import create_engine, Column, Integer, String, DateTime, func,Computed
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import bcrypt
from sqlalchemy import event


Base = declarative_base()


# Define the User Table model
class User(Base):
    __tablename__ = 'user_cred'

    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())



# CREATE TABLE Stocks (
#     stock_id SERIAL PRIMARY KEY,              -- Auto-incrementing ID for each stock entry
#     email VARCHAR(255),                       -- Foreign key reference to the Users table
#     stock_name VARCHAR(100),                  -- Name of the stock (e.g., 'AAPL', 'GOOG')
#     stock_value DECIMAL(10, 2),               -- Current value of the stock per share (e.g., $150.25)
#     initial_value DECIMAL(10, 2),             -- Initial value at the time of purchase (e.g., $120.50)
#     quantity INT,                             -- Number of shares the user holds
#     purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Date of purchase
#     FOREIGN KEY (email) REFERENCES Users(email) ON DELETE CASCADE
# );


class User_Fund(Base):

    __tablename__='user_fund'
    stock_id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, nullable=False)
    scheme_code=Column(String(200), unique=True, nullable=False)
    stock_name = Column(String(200), unique=True, nullable=False)
    initial_stock_value=Column(Integer, unique=True, nullable=False)
    current_value=Column(Integer, unique=True, nullable=False)
    quantity=Column(Integer, unique=True, nullable=False)
    gain = Column(Integer, Computed('(current_value - initial_stock_value) * quantity', persisted=True))
    purchased_at = Column(DateTime, default=func.now())


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


def insert_fund_family_details(scheme_Code,stock_name,curr_stock_value,scheme_type,mutual_fund_family):
    try:
        existing_scheme_code = session.query(Family_Fund_Details).filter(Family_Fund_Details.scheme_code == scheme_Code).first()
        if existing_scheme_code:
            existing_scheme_code.curr_stock_value=curr_stock_value

            session.commit()
            print("scheme id {scheme_code} already exists updted the latest value ")
            return
        else:
            # new_user = Family_Fund_Details(scheme_code=scheme_Code,stock_name=stock_name,curr_stock_value=curr_stock_value,
            #                                scheme_type=scheme_type,mutual_fund_family=mutual_fund_family)
            
            new_user=Family_Fund_Details(scheme_code=scheme_Code,stock_name=stock_name,curr_stock_value=curr_stock_value,
                                         scheme_type=scheme_type,mutual_fund_family=mutual_fund_family)
            session.add(new_user)
            session.commit()

    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close


@event.listens_for(Family_Fund_Details, 'after_update')
def update_user_table_on_family_fund_update(mapper, connection, target):
    if target.scheme_Code:  # Check if 'b' has been updated
        connection.execute(
            User_Fund.__tablename__.update()
            .where(User_Fund.scheme_Code == target.scheme_Code)  # Update Table2 where 'a' matches
            .values(current_value=target.curr_stock_value)  # Set 'b' to the updated value of Table1's 'b'
        )
      
