import sqlite3
import pandas as pd
from datetime import time as dt
import time 

#Connection to database
df = pd.read_csv(r'F:\Terminal Project\Database\finances_Updated.csv', encoding='latin1')
conn = sqlite3.connect('finances.db')
cur = conn.cursor()

#Creating Table
create_table = '''CREATE TABLE IF NOT EXISTS finances(
    DATE Datetime NOT NULL,
    DESCRIPTION VARCHAR(40),
    DEBIT INTEGER NOT NULL,
    CREDIT INTEGER NOT NULL,
    Sub_category VARCHAR(40) NOT NULL,
    CATEGORY VARCHAR(40),
    Transaction_Type VARCHAR(40),
    PENDING_TRANSACTION VARCHAR(40)
);'''

#Creating Table if it doesn't exist
cur.execute(create_table)

#Insert data from CSV into Database
df.to_sql('finances', conn, if_exists='replace', index=False)

