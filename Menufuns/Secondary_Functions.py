import os
from datetime import datetime
import time

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def option_input_function():
    option_input = input(' Enter option: ').strip()
    if not option_input:
        clear_terminal()
        return False 
    try:
        option_input = int(option_input)
        return option_input
    except ValueError:
        print('**Invalid Option**')
        return False 

def user_input_from_date():
    from_date_input = input(' Enter from date (YYYY-MM-DD): ').strip()
    if not from_date_input:
        clear_terminal()
        return None
    try:
        from_date = datetime.strptime(from_date_input, '%Y-%m-%d').date()
        return from_date
    except ValueError:
        clear_terminal()
        return False

def user_input_to_date():
    to_date_input = input(' Enter to date (YYYY-MM-DD): ').strip()
    if not to_date_input:
        clear_terminal()
        return None
    try:
        return datetime.strptime(to_date_input, '%Y-%m-%d').date()
    except ValueError:
        clear_terminal()
        return None
            
     
