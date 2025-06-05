#Libraries
from datetime import datetime as dt
import sqlite3 
import time 
from SQL_Functions.SQL_Connection import cur, conn, df, create_table 

#Creating Table if it doesn't exist
cur.execute(create_table)

#Insert data from CSV into Database
df.to_sql('finances', conn, if_exists='replace', index=False)

# #Getting first year in DB
# df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
# df_first_year = df['Date'].min().year


#Credits
def YTD_credits():
    current_year = dt.now().year
    current_date = dt.today().strftime('%Y-%m-%d')
    YTD_credit_SQL = f'''SELECT SUM(Credit)
    From finances 
    WHERE Date Between ? and ?
    '''
    cur.execute(YTD_credit_SQL, (f'{current_year}-01-01', current_date))
    YTD_credit_results = cur.fetchone()
    if YTD_credit_results and YTD_credit_results[0] is not None:
        print(f'    Total Credits Year-to-Date (YTD):')
        print(f'    ${YTD_credit_results[0]}')
        print()
    else:
        print('    No results found for the current year.')
        print()

def MTD_credits():
    current_month = dt.now().month
    current_month_str = f"{current_month:02d}"
    current_year = dt.now().year
    current_date = dt.today().strftime('%Y-%m-%d')
    MTD_credit_SQL = f'''SELECT SUM(Credit) 
    From finances 
    WHERE Date Between ? and ?
    '''
    cur.execute(MTD_credit_SQL,(f'{current_year}-{current_month_str}-01',current_date))
    MTD_credit_results = cur.fetchone()
    if MTD_credit_results and MTD_credit_results[0] is not None:
        print(f'    Total Credits Month-to-Date (MTD):')
        print(f'    ${MTD_credit_results[0]}')
        print()
    else:
        print('    No results found for the current month.')
        print()

def OAT_credits():
    OAT_credit_SQL = '''SELECT SUM(Credit) 
    From finances 
    '''
    cur.execute(OAT_credit_SQL)
    OAT_credit_results = cur.fetchone()
    if OAT_credit_results and OAT_credit_results[0] is not None:
        print(f'    Total Credits Of-All-Time (OAT):')
        print(f'    ${OAT_credit_results[0]}')
        print()
    else:
        print('    No results found for of all time.')
        print()

def Custom_credits(from_date,to_date):
    custom_credit_SQL = f'''SELECT SUM(Credit) 
    From finances 
    WHERE Date Between ? and ?
    '''
    cur.execute(custom_credit_SQL,(from_date, to_date))
    Custom_credit_results = cur.fetchone()
    if Custom_credit_results and Custom_credit_results[0] is not None:
        print(f'    Total Credits from {from_date} to {to_date}:')
        print(f'    ${Custom_credit_results[0]:,.2f}')
        print()
    else:
        print('    No results found for the current month.')
        print()

#Debits
def YTD_debits():
    current_year = dt.now().year
    current_date = dt.today().strftime('%Y-%m-%d')
    YTD_debit_SQL = f'''SELECT SUM(Debit) 
    From finances 
    WHERE Date Between ? and ?
    '''
    cur.execute(YTD_debit_SQL, (f'{current_year}-01-01', current_date))
    YTD_debits_results = cur.fetchone()
    if YTD_debits_results and YTD_debits_results[0] is not None:
        print(f'    Total Debits Year-to-Date (YTD):')
        print(f'    ${YTD_debits_results[0]:,.2f}')        
        print()
    else:
        print('    No results found for the current year.')
        print()

def MTD_debits():
    current_month = dt.now().month
    current_month_str = f"{current_month:02d}"
    current_year = dt.now().year
    current_date = dt.today().strftime('%Y-%m-%d')
    MTD_debit_SQL = f'''SELECT SUM(Credit) 
    From finances 
    WHERE Date Between ? and ?
    '''
    cur.execute(MTD_debit_SQL,(f'{current_year}-{current_month_str}-01',current_date))
    MTD_debit_results = cur.fetchone()
    if MTD_debit_results and MTD_debit_results[0] is not None:
        print(f'    Total Debit Month-to-Date (MTD):')
        print(f'    ${MTD_debit_results[0]}')
        print()
    else:
        print('    No results found for the current month.')
        print()

def OAT_debits():
    OAT_debits_SQL = '''SELECT SUM(Debit) 
    From finances 
    '''
    cur.execute(OAT_debits_SQL)
    OAT_debits_results = cur.fetchone()
    if OAT_debits_results and OAT_debits_results[0] is not None:
        print(f'    Total Debits Of-All-Time (OAT):')
        print(f'    ${OAT_debits_results[0]:,.2f}') 
        print()
    else:
        print('    No results found for of all time.')
        print()

def Custom_debit(from_date,to_date):
    custom_debit_SQL = f'''SELECT SUM(Debit) 
    From finances 
    WHERE Date Between ? and ?
    '''
    cur.execute(custom_debit_SQL,(from_date, to_date))
    Custom_debit_results = cur.fetchone()
    if Custom_debit_results and Custom_debit_results[0] is not None:
        print(f'    Total Debits from {from_date} to {to_date}:')
        print(f'    ${Custom_debit_results[0]:,.2f}')
        print() 
    else:
        print('    No results found for the current month.')
        print()

#Savings
def YTD_savings():
    current_year = dt.now().year
    current_date = dt.today().strftime('%Y-%m-%d')
    YTD_saving_SQL = f'''SELECT SUM(Credit) - SUM(Debit) 
    From finances 
    WHERE Date Between ? and ?
    '''
    cur.execute(YTD_saving_SQL, (f'{current_year}-01-01', current_date))
    YTD_savings_results = cur.fetchone()
    if YTD_savings_results and YTD_savings_results[0] is not None:
        print(f'    Total Savings Year-to-Date (YTD):')
        print(f'    ${YTD_savings_results[0]:,.2f}') 
        print()
    else:
        print('    No results found for the current year.')
        print()

def MTD_savings():
    current_month = dt.now().month
    current_month_str = f"{current_month:02d}"
    current_year = dt.now().year
    current_date = dt.today().strftime('%Y-%m-%d')
    MTD_saving_SQL = f'''SELECT SUM(Credit) - SUM(Debit) 
    From finances 
    WHERE Date Between ? and ?
    '''
    cur.execute(MTD_saving_SQL,(f'{current_year}-{current_month_str}-01',current_date))
    MTD_saving_results = cur.fetchone()
    if MTD_saving_results and MTD_saving_results[0] is not None:
        print(f'    Total Savings Month-to-Date (MTD):')
        print(f'    ${MTD_saving_results[0]:,.2f}')
        print()
    else:
        print('    No results found for the current month.')
        print()

def OAT_savings():
    current_date = dt.today().strftime('%Y-%m-%d')
    OAT_saving_SQL = '''SELECT SUM(Credit) - SUM(Debit) 
    From finances 
    '''
    cur.execute(OAT_saving_SQL)
    OAT_saving_results = cur.fetchone()
    if OAT_saving_results and OAT_saving_results[0] is not None:
        print(f'    Total Savings Of-All-Time (OAT):')
        print(f'    ${OAT_saving_results[0]:,.2f}')
        print()
    else:
        print('    No results found for of all time.')
        print()

def Custom_savings(from_date,to_date):
    custom_saving_SQL = f'''SELECT SUM(Credit) - Sum(Debit) 
    From finances 
    WHERE Date Between ? and ?
    '''
    cur.execute(custom_saving_SQL,(from_date, to_date))
    Custom_saving_results = cur.fetchone()
    if Custom_saving_results and Custom_saving_results[0] is not None:
        print(f'    Total Savings from {from_date} to {to_date}: ${Custom_saving_results[0]:,.2f}')
        print(f'    ${Custom_saving_results[0]:,.2f}')
        print()
    else:
        print('    No results found for the current month.')
        print()
