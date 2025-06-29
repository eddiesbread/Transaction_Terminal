from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import csv, os, json
from .forms import FinanceEntryForm 
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from collections import defaultdict
from calendar import month_abbr
from pathlib import Path

def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/Overview/')
        else:
            messages.error(request, "The username or password is incorrect.")
            return render(request, 'login.html')

    return render(request, 'login.html')

def overview(request):
    selected_year = request.GET.get("year", datetime.now().year)
    selected_year = int(selected_year)

    transactions = []
    monthly_income = defaultdict(float)
    monthly_expenses = defaultdict(float)

    csv_path = r'F:\Terminal Project\Database\finances_Updated.csv'  # Use raw string to avoid \f issue

    try:
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    date = datetime.strptime(row['Date'], "%d/%m/%Y %H:%M")
                except ValueError:
                    continue

                if date.year != selected_year:
                    continue

                try:
                    amount = float(row['Amount'])
                except ValueError:
                    continue

                month = date.strftime("%B")

                if amount >= 0:
                    monthly_income[month] += amount
                else:
                    monthly_expenses[month] += abs(amount)

                transactions.append({
                    "date": date.strftime("%d/%m/%Y"),
                    "description": row['Description'],
                    "amount": f"${amount:.2f}"
                })
    except FileNotFoundError:
        pass

    month_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    chart_labels = month_order
    income_data = [round(monthly_income.get(month, 0), 2) for month in month_order]
    expenses_data = [round(monthly_expenses.get(month, 0), 2) for month in month_order]

    total_income = sum(income_data)
    total_expenses = sum(expenses_data)
    savings = total_income - total_expenses

    context = {
        "selected_year": selected_year,
        "years": list(range(2020, datetime.now().year + 1)),
        "total_income": f"${total_income:,.2f}",
        "total_expenses": f"${total_expenses:,.2f}",
        "savings": f"${savings:,.2f}",
        "recent_transactions": transactions[-5:][::-1],
        "chart_labels": chart_labels,
        "income_data": income_data,
        "expenses_data": expenses_data
    }

    return render(request, "overview.html", context)

@csrf_exempt
@login_required
def data_entry(request):
    if request.method == 'POST':
        raw_date = request.POST.get('entry_date')
        current_time = datetime.now().strftime('%H:%M')
        formatted_date = datetime.strptime(raw_date, '%Y-%m-%d').strftime('%d/%m/%Y') + f' {current_time}'

        amount = float(request.POST.get('amount'))
        description = request.POST.get('description')
        transaction_type = request.POST.get('transaction_type')
        category = request.POST.get('category')
        subcategory = request.POST.get('subcategory')

        credit = amount if transaction_type == 'Credit' else 0
        debit = amount if transaction_type == 'Debit' else 0
        amount_signed = credit - debit

        csv_path = r'F:\Terminal Project\Database\finances_Updated.csv'
        file_exists = os.path.isfile(csv_path)

        with open(csv_path, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            if not file_exists:
                writer.writerow([
                    'Date', 'Description', 'Debit', 'Credit', 'Amount',
                    'Sub-category', 'Category', 'Transaction Type'
                ])
            writer.writerow([
                formatted_date, description, debit, credit, amount_signed,
                subcategory, category, 'Expense' if transaction_type == 'Debit' else 'Credit'
            ])

        return redirect('/Data_entry/')

    return render(request, 'data_entry.html')

@login_required
def expenses(request):
    response = render(request, 'expenses.html')
    response['Cache-Control'] = 'no-store'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

@login_required
def database(request):
    csv_path = r'F:\Terminal Project\Database\finances_Updated.csv'
    data = []

    try:
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        headers = []
        data = []

    response = render(request, 'database.html', {
        'headers': headers,
        'data': data
    })
    response['Cache-Control'] = 'no-store'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

def logout_view(request):
    logout(request)
    response = redirect('/')
    response['Cache-Control'] = 'no-store'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response