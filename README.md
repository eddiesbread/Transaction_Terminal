#  Transaction Terminal

**Transaction Terminal** is a hybrid CLI + web-based finance manager built in Python. It processes and analyzes transaction records stored in an SQLite database and CSV files. The terminal interface allows quick data entry and analytics, while the Django dashboard provides a clean web-based visualization of your finances.

---

##  Features

### 🖥 Terminal Interface
- Add transactions (credit, debit, savings) via command line
- Date filtering (YTD, MTD, custom range)
- Quick statistics and summaries
- Clean menu-driven navigation

###  Django Web Dashboard
- Start the dashboard directly from the terminal menu
- View total monthly income/expenses
- See visual charts comparing income and expenses
- Recent transaction list

###  Backend
- Dual data storage using:
  - SQLite (`db.sqlite3`)
  - CSV (`finances_Updated.csv`)
- Modular architecture with SQL query logic separated in `SQL_Functions/`

---

##  Prerequisites

- Python 3.9+
- SQLite3

