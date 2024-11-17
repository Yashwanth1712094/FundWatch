import os

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