from django import forms

class FinanceEntryForm(forms.Form):
    entry_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    description = forms.CharField(widget=forms.Textarea)
    category = forms.ChoiceField(choices=[
        ('Salary', 'Salary'),
        ('Transport', 'Transport'),
        ('Eating', 'Eating'),
        ('Shopping', 'Shopping'),
        ('Entertainment', 'Entertainment'),
        ('Groceries', 'Groceries'),
        ('Undef', 'Undef'),
        ('Investments', 'Investments'),
        ('Business', 'Business'),
        ('Membership', 'Membership'),
        ('Rent', 'Rent'),
        ('Reimbursements', 'Reimbursements'),
        ('Dividends', 'Dividends')
    ])
    subcategory = forms.ChoiceField(choices=[
        ('Salary', 'Salary'),
        ('Dividends', 'Dividends'),
        ('Other Incomes', 'Other Incomes'),
        ('Car Installments', 'Car Installments'),
        ('Fuel', 'Fuel'),
        ('Public Transport', 'Public Transport'),
        ('Work Transport', 'Work Transport'),
        ('Café', 'Café'),
        ('Eating Out', 'Eating Out'),
        ('Bar', 'Bar'),
        ('Shopping', 'Shopping'),
        ('Entertainment', 'Entertainment'),
        ('Fees', 'Fees'),
        ('Cash', 'Cash'),
        ('Investments', 'Investments'),
        ('Memberships', 'Memberships'),
        ('Undef', 'Undef'),
        ('Business', 'Business'),
        ('Rent', 'Rent'),
        ('Phone Bill', 'Phone Bill'),
        ('Reimbursements', 'Reimbursements')
    ])
    pending_transaction = forms.BooleanField(required=False)