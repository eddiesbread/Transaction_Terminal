#Date Menu
def To_Date_Menu(from_date,account_type):
    function_map = {'Credit':Custom_credits,'Debit':Custom_debit,'Saving':Custom_savings}
    while True:
        print('--------------------------------------------------------')
        print('                Transaction Terminal                   ')
        print('--------------------------------------------------------')
        print(f'   From date entered: {from_date}')         
        print()
        print('--------------------------------------------------------')
        print()
        to_date = user_input_to_date()
        print()

        if to_date <= from_date:
            print(f'Please use to-date greater than {from_date}')
            time.sleep(1.5)
            clear_terminal()
            continue
        else:
            clear_terminal()
            print('--------------------------------------------------------')
            print('                Transaction Terminal                   ')
            print('--------------------------------------------------------')
            print(f'   From date entered: {from_date}')         
            print(f'   From date entered: {to_date}')   
            print()
            print('   Do you want to proceed with this date:')
            print()
            print('   [Y] Yes')
            print('   [N] No')
            print()
            print('--------------------------------------------------------')
            print()
            proceed = input('   Enter option: ').strip().upper()
            if proceed == 'Y':
                clear_terminal()
                function_map[account_type](from_date, to_date)
                break
            #enter values
            elif proceed == 'N':
                clear_terminal()
                From_Date_Menu()
                break
            else:
                print('Invalid option. Please enter "Y" or "N".')


def From_Date_Menu():
    while True:
        print('--------------------------------------------------------')
        print('                Transaction Terminal                   ')
        print('--------------------------------------------------------')
        print('    Enter From Date: ')        
        print()
        print('--------------------------------------------------------')
        print()
        from_date = user_input_from_date()

        if not from_date:
            print('--------------------------------------------------------')
            print('                Transaction Terminal                   ')
            print('--------------------------------------------------------')
            print('    Enter From Date: ')        
            print()
            print('--------------------------------------------------------')
            print()
            print('Please use a date using YYYY-MM-DD format.')
            time.sleep(2.0)
            clear_terminal()
            continue
        else:
            clear_terminal()
            To_Date_Menu(from_date)
            break