
# global_variable.py
global_email = None

def set_variable(value):
    global global_email
    global_email = value

def get_variable():
    return global_email


# other_module.py
# import global_variable

# # Set global variable
# global_variable.set_variable("Global variable set")

# # Access global variable
# print(global_variable.get_variable())  # Output: Global variable set
