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
        return False
    try:
        return from_date_input.strftime(from_date_input, '%Y-%m-%d')
    except ValueError:
        clear_terminal()

def user_input_to_date():
    to_date_input = input(' Enter to date (YYYY-MM-DD): ').strip()
    if not to_date_input:
        clear_terminal()
        return False
    try:
        return to_date_input.strftime(to_date_input, '%Y-%m-%d')
    except ValueError:
        return False

class InputManager:
    def __init__(self):
        pass

    def T_Date(self, account_type):
        while True:
            T_Date_Input = input( 'Enter date (YYYY-MM-DD): ').strip()
            if not T_Date_Input:
                clear_terminal()
                return None
            elif T_Date_Input > datetime.today().strftime('%Y-%m-%d'):
                clear_terminal()
                return None            
            try:
                date_obj = datetime.strptime(T_Date_Input, '%Y-%m-%d')
                return date_obj.date()
            except ValueError:
                clear_terminal()
                return False
            
    def T_Description(self, account_type):
        while True:
            T_Description_Input = input(' Enter description of transcation: ').strip()
            if not T_Description_Input:
                clear_terminal()
                return False
            try:
                return T_Description_Input
            except ValueError:
                clear_terminal()
                return False 
            
    def T_Credit(self, account_type):
        while True:
            T_Credit_Input = input(' Enter amount CR of transcation: ').strip()
            if not T_Credit_Input:
                clear_terminal()
                return False
            try:
                T_Credit_Input = int(T_Credit_Input)
                return T_Credit_Input
            except ValueError:
                clear_terminal()
                return False 

    def T_Debit(self, account_type):
        while True:
            T_Debit_Input = input(' Enter amount DR of transcation: ').strip()
            if not T_Debit_Input:
                clear_terminal()
                return False
            try:
                T_Debit_Input = int(T_Debit_Input)
                return T_Debit_Input
            except ValueError:
                clear_terminal()
                return False 

    def T_Category(self, account_type):
        allowed_categories = [
            'Salary', 'Transport', 'Eating', 'Shopping', 'Entertainment',
            'Groceries', 'Undef', 'Investments', 'Business', 'Membership',
            'Rent', 'Reimbursements', 'Dividends'
        ]

        while True:
            T_Category_Input = input('Enter category of transaction: ').strip()
            if not T_Category_Input:
                clear_terminal()
                return False
            elif T_Category_Input in allowed_categories:
                return T_Category_Input
            else:
                clear_terminal()
                return False 
            
    def T_Sub_category(self, account_type):
        allowed_Sub_categories = [
            'Salary', 'Dividends', 'Other Incomes ', 'Car Installments', 'Fuel ',
            'Public Transport', 'Work Transport', 'Café', 'Eating Out', 'Bar',
            'Shopping', 'Entertainment', 'Fees', 'Cash', 'Investments', 'Memberships',
            'Undef', 'Business', 'Rent', 'Phone Bill', 'Reimbursements'
        ]

        while True:
            T_Sub_category_Input = input('Enter Sub_category of transaction: ').strip()
            if not T_Sub_category_Input:
                clear_terminal()
                return False
            elif T_Sub_category_Input in allowed_Sub_categories:
                return T_Sub_category_Input
            else:
                clear_terminal()
                return False 
            
    def T_Pending_transaction(self, account_type):
        while True:
            Pending_transaction_Input = input('Pending Transaction? [Y/N]: ').strip().upper()
            if Pending_transaction_Input == 'Y':
                clear_terminal()
                return True
            elif Pending_transaction_Input == 'N':
                clear_terminal()
                return "False"
            
            else:
                clear_terminal()
                return False
    
    # def T_Transaction_confirm(self, account_type):
    #     while True:
    #         Pending_transaction_Input = input('Confirm Transaction [Y/N]: ').strip().upper()
    #         if Pending_transaction_Input == 'Y':
    #             clear_terminal()
    #             return True
    #         elif Pending_transaction_Input == 'N':
    #             clear_terminal()
    #             return "False"
            
    #         else:
    #             clear_terminal()
    #             return False