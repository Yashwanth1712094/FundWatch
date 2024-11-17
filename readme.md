step-1: install python virtual environment
        -- python3.10 -m venv venv
        --source venv/bin/actiate

step-2: create 1 postgres table for signup and login
        pip install sqlalchemy psycopg2 bcrypt
        postgres installation steps  in ubuntu

        --sudo apt update
        --sudo apt upgrade
        --sudo apt install postgresql postgresql-contrib
        --psql --version
        --sudo systemctl start postgresql
        --sudo systemctl enable postgresql
        --sudo systemctl status postgresql
        --sudo -i -u postgres
        --psql
        


