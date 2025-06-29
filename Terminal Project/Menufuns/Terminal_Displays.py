#Libraries
import time 
import sqlite3 
import pandas as pd
import os
from datetime import datetime
from Menufuns.Secondary_Functions import clear_terminal, option_input_function, user_input_from_date, user_input_to_date, InputManager
from SQL_Functions.SQL_Statements import YTD_credits,MTD_credits,OAT_credits, YTD_debits, MTD_debits, OAT_debits, YTD_savings, MTD_savings, OAT_savings, Custom_credits, Custom_debit, Custom_savings
from SQL_Functions.SQL_Connection import cur
from django.core.management import execute_from_command_line
import sys

class MenuManger:
    def __init__(self):
        self.account_types = {1:'credit',2: 'debit',3: 'savings'}
    
    def main_menu(self): #Primary Funciton Menu 
        while True:
            print_terminal_header('MAIN MENU')
            print('    Select from the following options: ')
            print()
            print('    [1] Enter Transactions')
            print('    [2] Analysis Center')
            print('    [3] Exit Program')
            print()
            print('═══════════════════════════════════════════════════')
            print()
            
            option_input = option_input_function()
            if option_input == 1:
                clear_terminal()
                transaction = Transaction(None, None, 0.0, 0.0, 0.0, None, None, None, None)
                transaction.Transaction_account_select()
                break
            elif option_input == 2:
                clear_terminal()
                sys.path.append(r"F:\Terminal Project\finapp")
                os.environ.setdefault("DJANGO_SETTINGS_MODULE", "finapp.settings")
                os.chdir(r"F:\Terminal Project\finapp")
                try:
                    execute_from_command_line(["manage.py", "runserver", "127.0.0.1:8001"])
                except Exception as e:
                    print("Failed to run Django app:", e)
                    input("Press Enter to return to menu...")
                    clear_terminal()

    def sec_menu(self): #Account Handler 
        while True:
            print_terminal_header('ACCOUNT SELECTION')
            print('    Please select an account type: ')
            print()
            for key, val in self.account_types.items():
                print(f'    [{key}] {val.capitalize()}')
            print('    [4] Back to Main Menu')
            print()
            print('═══════════════════════════════════════════════════')
            print() 
            
            option_input = option_input_function()
            if option_input in self.account_types:
                clear_terminal()
                self.account_menu(self.account_types[option_input])
                break
            elif option_input == 4:
                clear_terminal()
                self.main_menu()
            else:
                clear_terminal()

    def account_menu(self,account_types):
        while True:
            print_terminal_header(f'{account_types.capitalize()} Account Menu')
            print('    Select a reporting option:')
            print()
            print('    [1] Year-to-Date (YTD)')
            print('    [2] Month-to-Date (MTD)')
            print('    [3] Overall-All-Time (OAT)')
            print('    [4] Custom Date Range')
            print('    [5] Back to Account Selection')
            print()
            print('═══════════════════════════════════════════════════')
            print()
            
            option_input = option_input_function()

            if option_input in [1, 2, 3]:
                report_key = {1:'YTD',2:'MTD',3:'OAT'}[option_input]
                clear_terminal()
                print_terminal_header(f'{account_types.capitalize()} Reporting Manager') 
                print()
                report_manager = SQLReportingManager(account_types)
                report_manager.run_report(report_key, ())
                print('═══════════════════════════════════════════════════')
                input('Press enter to return to menu...')  
                clear_terminal()
                self.sec_menu() 
                break 
            elif option_input == 4:
                clear_terminal()
                date_range = DateRangeSelector(account_types).From_Date_Menu()
                if date_range:
                    from_date, to_date = date_range
                    clear_terminal()
                    print_terminal_header('Reporting Manager')
                    print()
                    report_manager = SQLReportingManager(account_types)
                    report_manager.run_report('Custom', (from_date, to_date))
                    print('═══════════════════════════════════════════════════')
                    input('Press enter to return to menu...')
                    clear_terminal()                
                    self.sec_menu() 
            elif option_input == 5:
                clear_terminal()
                self.sec_menu()
                break
            else:
                clear_terminal()
                self.account_menu(account_types)

#SQL Report Handler
class SQLReportingManager:
    def __init__(self, account_types):
        self.account_types = account_types
        self.reportingmap = {
            'credit': {
                'YTD': YTD_credits,
                'MTD': MTD_credits,
                'OAT': OAT_credits,
                'Custom': Custom_credits
            },
            'debit': {
                'YTD': YTD_debits,
                'MTD': MTD_debits,
                'OAT': OAT_debits,
                'Custom': Custom_debit
            },        
            'savings': {
                'YTD': YTD_savings,
                'MTD': MTD_savings,
                'OAT': OAT_savings,
                'Custom': Custom_savings
            },
        }

    def run_report(self, reporting_type,args):
        func = self.reportingmap[self.account_types][reporting_type]
        return func(*args)

#Date Handler
class DateRangeSelector:
    def __init__(self, account_types):
        self.account_types = account_types
        
    def From_Date_Menu(self):
        while True:
            print_terminal_header(f'{self.account_types.capitalize()} Reporting Manager')
            print()
            print('    Enter From Date: ')        
            print()
            print('═══════════════════════════════════════════════════')
            print()
            from_date = user_input_from_date()

            if from_date:
                clear_terminal()
                to_date = self.To_Date_Menu(from_date)
                if to_date:
                    return from_date, to_date

    def To_Date_Menu(self,from_date):
        while True:
            print_terminal_header(f'{self.account_types.capitalize()} Reporting Manager')
            print()
            print(f'   To date entered: {from_date}')         
            print()
            print('═══════════════════════════════════════════════════')
            print()
            to_date = user_input_to_date()

            if not to_date:
                clear_terminal()
                continue
            if to_date < from_date:
                print(f' {to_date.strftime('%Y-%m-%d')} must be after {from_date.strftime('%Y-%m-%d')}')
                time.sleep(1.5)
                clear_terminal()
                continue
            else:
                clear_terminal()
                if self.Date_Confirmnation(from_date, to_date):
                    return to_date

    def Date_Confirmnation(self, from_date, to_date):
        while True:
            print_terminal_header(f'{self.account_types.capitalize()} Reporting Manager')
            print()
            print(f'   Custom Range: {from_date} to {to_date}')           
            print()
            print('   Do you wish to proceed?:')
            print()
            print('   [Y] Yes')
            print('   [N] No')
            print()
            print('═══════════════════════════════════════════════════')
            print()
            proceed = input('   Enter option: ').strip().upper()
            if proceed == 'Y':
                clear_terminal()
                return True
            elif proceed == 'N':
                clear_terminal()
                self.From_Date_Menu()
                continue
            else:
                continue

#Terminal Header
def print_terminal_header(title):
    print('═══════════════════════════════════════════════════')
    print(f'    {title.center(48)}')
    print('═══════════════════════════════════════════════════')

#Transaction Account
class Transaction:
    def __init__(self, Date, Description, Debit, Credit, Amount, Sub_category, Category, Transaction_Type, Account_type):
        self.Date = Date
        self.Description = Description
        self.Debit = Debit
        self.Credit = Credit
        self.Amount = Amount
        self.Sub_category = Sub_category
        self.Category = Category
        self.Transaction_Type = Transaction_Type
        self.Account_type = Account_type

    def Transaction_account_select(self):
        while True:
            print_terminal_header('Transaction Center')
            print('    Select the account: ')
            print()
            print('    [1] Credit')
            print('    [2] Debit')
            print('    [3] Main Menu')
            print()
            print('═══════════════════════════════════════════════════') 
            print()

            option_input = option_input_function()
            if option_input == 1:
                clear_terminal()
                self.Create_Transaction_Date('credit')
                break
            if option_input == 2:
                clear_terminal()
                self.Create_Transaction_Date('debit')
                break
            if option_input == 3:
                clear_terminal()
                MenuManger().main_menu()
                break
            else:
                clear_terminal()
    
    def Create_Transaction_Date(self, account_type):
        while True:
            self.Account_type = account_type
            print_terminal_header(f'Account: {account_type.capitalize()}')
            print()
            print('    Date of Transcation (YYYY-MM-DD): ')
            print('    Description: ')
            print('    Amount: $')
            print('    Category: ')
            print('    Sub_category: ')           
            print()
            print('═══════════════════════════════════════════════════') 
            print()
            input_manager = InputManager()
            self.Date = input_manager.T_Date(account_type)
            if self.Date:
                clear_terminal()
                self.Create_Transaction_Description(account_type)
                break

    def Create_Transaction_Description(self,account_type):
            while True:
                self.Account_type = account_type
                print_terminal_header(f'Account: {account_type.capitalize()}')
                print()
                print(f'    Date of Transcation (YYYY-MM-DD): {self.Date}')
                print('    Description: ')
                print('    Amount: $')
                print('    Category: ')
                print('    Sub_category: ') 
                print()
                print('═══════════════════════════════════════════════════') 
                print()
                input_manager = InputManager()
                self.Description = input_manager.T_Description(account_type)
                if self.Description:
                    clear_terminal()
                    if account_type == 'credit':
                        self.Create_Transaction_Credit(account_type)
                        break
                    else:
                        self.Create_Transaction_Debit(account_type)
                    break

    def Create_Transaction_Debit(self,account_type):
        while True:
                self.Account_type = account_type
                print_terminal_header(f'Account: {account_type.capitalize()}')
                print()
                print(f'    Date of Transcation (YYYY-MM-DD): {self.Date}')
                print(f'    Description: {self.Description}')
                print('    Amount: $')
                print('    Category: ')
                print('    Sub_category: ') 
                print()
                print('═══════════════════════════════════════════════════') 
                print() 
                input_manager = InputManager()
                self.Debit = input_manager.T_Debit(account_type) 
                self.Credit = 0.0
                self.Transaction_Type = 'Expense'
                if self.Debit:
                    self.Amount = self.Credit - self.Debit 
                    clear_terminal()
                    self.Create_Transaction_Category(account_type)
                    break

    def Create_Transaction_Credit(self,account_type):
        while True:
                self.Account_type = account_type
                print_terminal_header(f'Account: {account_type.capitalize()}')
                print()
                print(f'    Date of Transcation (YYYY-MM-DD): {self.Date}')
                print(f'    Description: {self.Description}')
                print('    Amount: $')
                print('    Category: ')
                print('    Sub_category: ') 
                print()
                print('═══════════════════════════════════════════════════') 
                print()
                input_manager = InputManager()
                self.Credit = input_manager.T_Credit(account_type)
                self.Debit = 0.0
                self.Transaction_Type = 'Income'
                if self.Credit:
                    clear_terminal()
                    self.Amount = self.Credit - self.Debit
                    self.Create_Transaction_Category(account_type)
                    break

    def Create_Transaction_Category(self,account_type):
            while True:
                self.Account_type = account_type
                print_terminal_header(f'Account: {account_type.capitalize()}')
                print()
                print(f'    Date of Transcation (YYYY-MM-DD): {self.Date}')
                print(f'    Description: {self.Description}')
                if account_type == 'credit':
                    print(f'    Amount: ${self.Credit}')
                else:
                    print(f'    Amount: ${self.Debit}')
                print('    Category: ')
                print('    Sub_category: ')
                print()
                print('═══════════════════════════════════════════════════') 
                print()
                input_manager = InputManager()
                self.Category = input_manager.T_Category(account_type)
                if self.Category:
                    clear_terminal()
                    self.Create_Transaction_T_Sub_category(account_type)

    def Create_Transaction_T_Sub_category(self,account_type):
            while True:
                self.Account_type = account_type
                print_terminal_header(f'Account: {account_type.capitalize()}')
                print()
                print(f'    Date of Transcation (YYYY-MM-DD): {self.Date}')
                print(f'    Description: {self.Description}')
                if account_type == 'credit':
                    print(f'    Amount: ${self.Credit}')
                else:
                    print(f'    Amount: ${self.Debit}')
                print(f'    Category: {self.Category}')
                print(f'    Sub_category: ')
                print()
                print('═══════════════════════════════════════════════════') 
                print()
                input_manager = InputManager()
                self.Sub_category = input_manager.T_Sub_category(account_type)
                if self.Sub_category:
                    clear_terminal()
                    self.Create_Transaction_Confirm(account_type)

    def Create_Transaction_Confirm(self,account_type):
        while True:
            self.Account_type = account_type
            print_terminal_header(f'Account: {account_type.capitalize()}')
            print()
            print(f'    Date of Transcation (YYYY-MM-DD): {self.Date}')
            print(f'    Description: {self.Description}')
            if account_type == 'credit':
                print(f'    Amount: ${self.Credit}')
            else:
                print(f'    Amount: ${self.Debit}')
            print(f'    Category: {self.Category}')
            print(f'    Sub_category: {self.Sub_category}') 
            print()
            print('═══════════════════════════════════════════════════') 
            print()
            
            confirm = input('Confirm Transaction [Y/N]: ').strip().upper()
            if confirm == 'Y':
                clear_terminal()
                self.Save_to_csv()
                break
            elif confirm == 'N':
                clear_terminal()
                break
            else:
                clear_terminal()

    def Save_to_csv(self, filename=r'F:\Terminal Project\Database\finances_Updated.csv'):
        if not os.path.isfile(filename):
            print_terminal_header(f'Account: {self.Account_type.capitalize()}')
            print()
            print(f"CSV file '{filename}' does not exist. Transaction not saved.")
            print()
            print('═══════════════════════════════════════════════════')
            input('Press Enter to return to menu...')
            clear_terminal()
            MenuManger().main_menu()
            return
        
        if isinstance(self.Date, datetime):
            date_str = self.Date.strftime('%d/%m/%Y 0:00')
        else:
            try:
                dt = datetime.strptime(self.Date, '%Y-%m-%d')
                date_str = dt.strftime('%d/%m/%Y 0:00')
            except Exception:
                date_str = self.Date   

        data = {
            'Date': [date_str],  
            'Description': [self.Description],
            'Debit': [self.Debit],
            'Credit': [self.Credit],
            'Amount': [self.Amount],
            'Sub_category': [self.Sub_category],
            'Category': [self.Category],
            'Transaction_Type': [self.Transaction_Type],
        }
        df = pd.DataFrame(data)
        df.to_csv(filename, mode='a', index=False, header=False)

        print_terminal_header(f'Account: {self.Account_type.capitalize()}')
        print()
        print('\nTransaction saved successfully.')
        print()
        print('═══════════════════════════════════════════════════')
        print()
        input('Press Enter to return to menu...')
        clear_terminal()
        MenuManger().main_menu()