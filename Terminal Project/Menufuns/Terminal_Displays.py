#Libraries
import time 
import sqlite3 
import pandas as pd
from Menufuns.Secondary_Functions import clear_terminal, option_input_function, user_input_from_date, user_input_to_date
from SQL_Functions.SQL_Statements import YTD_credits,MTD_credits,OAT_credits, YTD_debits, MTD_debits, OAT_debits, YTD_savings, MTD_savings, OAT_savings, Custom_credits, Custom_debit, Custom_savings
from SQL_Functions.SQL_Connection import cur


#Primary menu
def main_menu():
    while True:
        print()
        print_terminal_header()
        print('    Select from the following: ')
        print()
        print('    [1] Enter Program')
        print('    [2] Exit Program')
        print('    [3] Help')
        print()
        print('--------------------------------------------------------')
        print()

        option_input = option_input_function()
        if option_input == 1:
            clear_terminal()
            sec_menu()
        elif option_input == 2:
            print('Closing Program...')
            cur.close()
            time.sleep(2.5)
            clear_terminal()
            exit()
        elif option_input == 3:
            clear_terminal()
            pass
        else:
            clear_terminal()

#Secondary Menu (Account Type Selection)
def sec_menu():
    while True:
        print_terminal_header()
        print('    Select the account: ')
        print()
        print('    [1] Credit')
        print('    [2] Debit')
        print('    [3] Saving')
        print('    [4] Back to main menu')
        print()
        print('--------------------------------------------------------')
        print() 
        
        option_input = option_input_function()
        if option_input in [1,2,3]:
            account_types = {1:'credit',2:'debit',3:'savings'}
            clear_terminal()
            account_menu(account_types[option_input])
            break
        elif option_input == 4:
            clear_terminal()
            main_menu()
        else:
            clear_terminal()
            sec_menu()

#Universal Account Menu Handler
def account_menu(account_types):
    account_map = {
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
    while True:
        print_terminal_header()
        print(f'    Account: {account_types.capitalize()}')
        print('    Select the following:')
        print()
        print('    [1] YTD')
        print('    [2] MTD')
        print('    [3] OAT')
        print('    [4] Custom Date Range')
        print('    [5] Back to Accounts')
        print()
        print('--------------------------------------------------------')
        print()
        
        option_input = option_input_function()

        if option_input in [1, 2, 3]:
            account_keys = {1:'YTD',2:'MTD',3:'OAT'}[option_input]
            clear_terminal()
            print_terminal_header()   
            print()
            account_map[account_types][account_keys]()
            print('--------------------------------------------------------')
            input('Press enter to return to menu...')  
            clear_terminal()
            sec_menu() 
            break 
        if option_input == 4:
            clear_terminal()
            date_range = From_Date_Menu(account_types)
            if date_range:
                from_date, to_date = date_range
                clear_terminal()
                print_terminal_header()
                account_map[account_types]['Custom'](from_date,to_date)
                print('--------------------------------------------------------')
                input('Press enter to return to menu...')
                clear_terminal()                
                sec_menu() 
            break
        if option_input == 5:
            clear_terminal()
            sec_menu()
            break
        else:
            clear_terminal()
            account_menu(account_types)

#Date handler
def To_Date_Menu(from_date,account_types):
    while True:
        print_terminal_header()
        print(f'   To date entered: {from_date}')         
        print()
        print('--------------------------------------------------------')
        print()
        to_date = user_input_to_date()
        print()

        if to_date < from_date:
            print(f'{to_date} must be after {from_date}')
            time.sleep(1.5)
            clear_terminal()
            continue
        else:
            clear_terminal()
            print_terminal_header()
            print(f'   Custom Range: {from_date} to {to_date}')           
            print()
            print('   Do you wish to proceed?:')
            print()
            print('   [Y] Yes')
            print('   [N] No')
            print()
            print('--------------------------------------------------------')
            print()
            proceed = input('   Enter option: ').strip().upper()
            if proceed == 'Y':
                clear_terminal()
                return to_date
            elif proceed == 'N':
                clear_terminal()
                From_Date_Menu(account_types)
                continue
            else:
                print('Invalid option. Please enter "Y" or "N".')


def From_Date_Menu(account_types):
    while True:
        print_terminal_header()
        print('    Enter From Date: ')        
        print()
        print('--------------------------------------------------------')
        print()
        from_date = user_input_from_date()

        if from_date:
            clear_terminal()
            to_date = To_Date_Menu(from_date,account_types)
            if to_date:
                return from_date, to_date

#Terminal Header
def print_terminal_header():
    print('--------------------------------------------------------')
    print('                Transaction Terminal                   ')
    print('--------------------------------------------------------')