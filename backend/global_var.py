'''
This file keeps the track of logged in email

'''
# global_variable.py
global_email = None

def set_variable(value):
    global global_email
    global_email = value

def get_variable():
    return global_email


