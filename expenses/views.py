from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.utils import timezone
from .models import Expense, Income
from .forms import ExpenseForm, IncomeForm
import csv
import io
import xlsxwriter
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from django.db.models import Sum
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.db.models import Sum, F

User = get_user_model()

@login_required
def expense_list(request):
    income_list = Income.objects.filter(user=request.user)
    expense_list = Expense.objects.filter(user=request.user)
    total_income = income_list.aggregate(total_income=Sum('amount'))['total_income'] or 0
    total_expense = expense_list.aggregate(total_expense=Sum('amount'))['total_expense'] or 0
    balance = total_income - total_expense

    context = {
        'income_list': income_list,
        'expense_list': expense_list,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
    }
    
    return render(request, 'expenses/expense_list.html', context)

@login_required
def expense_create(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'expenses/expense_form.html', {'form': form})

@login_required
def expense_edit(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'expenses/expense_form.html', {'form': form})

@login_required
def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        expense.delete()
        return redirect('expense_list')
    return render(request, 'expenses/expense_confirm_delete.html', {'object': expense})

@login_required
def export_expenses_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="expenses.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Title', 'Amount', 'Date', 'Category', 'Description'])
    
    expenses = Expense.objects.filter(user=request.user)
    for expense in expenses:
        writer.writerow([expense.title, expense.amount, expense.date, expense.category, expense.description])
    
    return response

@login_required
def export_expenses_excel(request):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()
    columns = ['ID', 'Title', 'Amount', 'Date', 'Category', 'Description']
    for col_num, header in enumerate(columns):
        worksheet.write(0, col_num, header)
    expenses = Expense.objects.filter(user=request.user)
    for row_num, expense in enumerate(expenses, 1):
        worksheet.write(row_num, 0, expense.id)
        worksheet.write(row_num, 1, expense.title)
        worksheet.write(row_num, 2, expense.amount)
        worksheet.write(row_num, 3, expense.date.strftime('%Y-%m-%d'))
        worksheet.write(row_num, 4, expense.category)
        worksheet.write(row_num, 5, expense.description)
    workbook.close()
    output.seek(0)
    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="expenses.xlsx"'
    return response

@login_required
def export_expenses_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="expenses.pdf"'
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    expenses = Expense.objects.filter(user=request.user)
    data = [['Title', 'Amount', 'Date', 'Category', 'Description']]
    for expense in expenses:
        data.append([expense.title, expense.amount, expense.date, expense.category, expense.description])
    
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), '#d5d5d5'),
        ('TEXTCOLOR', (0, 0), (-1, 0), '#000000'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), '#f5f5f5'),
        ('GRID', (0, 0), (-1, -1), 1, '#000000'),
    ]))
    elements.append(table)
    doc.build(elements)
    buffer.seek(0)
    response.write(buffer.read())
    
    return response

@login_required
def income_list(request):
    incomes = Income.objects.filter(user=request.user).order_by('-date')
    return render(request, 'expenses/income_list.html', {'incomes': incomes})

@login_required
def income_create(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            return redirect('expense_list')
    else:
        form = IncomeForm()
    return render(request, 'expenses/income_form.html', {'form': form})

@login_required
def income_update(request, pk):
    income = get_object_or_404(Income, pk=pk, user=request.user)
    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = IncomeForm(instance=income)
    return render(request, 'expenses/income_form.html', {'form': form})

@login_required
def income_delete(request, pk):
    income = get_object_or_404(Income, pk=pk, user=request.user)
    if request.method == 'POST':
        income.delete()
        return redirect('expense_list')
    return render(request, 'expenses/income_confirm_deletee.html', {'income': income})
@login_required
def export_income_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="income.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Title', 'Amount', 'Date', 'Source', 'Description'])
    
    income_list = Income.objects.filter(user=request.user)
    for income in income_list:
        writer.writerow([income.title, income.amount, income.date, income.source, income.description])
    
    return response

@login_required
def export_income_excel(request):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()
    columns = ['ID', 'Title', 'Amount', 'Date', 'Source', 'Description']
    for col_num, header in enumerate(columns):
        worksheet.write(0, col_num, header)
    income_list = Income.objects.filter(user=request.user)
    for row_num, income in enumerate(income_list, 1):
        worksheet.write(row_num, 0, income.id)
        worksheet.write(row_num, 1, income.title)
        worksheet.write(row_num, 2, income.amount)
        worksheet.write(row_num, 3, income.date.strftime('%Y-%m-%d'))
        worksheet.write(row_num, 4, income.source)
        worksheet.write(row_num, 5, income.description)
    workbook.close()
    output.seek(0)
    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="income.xlsx"'
    return response

@login_required
def export_income_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="income.pdf"'
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    income_list = Income.objects.filter(user=request.user)
    data = [['Title', 'Amount', 'Date', 'Source', 'Description']]
    for income in income_list:
        data.append([income.title, income.amount, income.date, income.source, income.description])
    
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), '#d5d5d5'),
        ('TEXTCOLOR', (0, 0), (-1, 0), '#000000'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), '#f5f5f5'),
        ('GRID', (0, 0), (-1, -1), 1, '#000000'),
    ]))
    elements.append(table)
    doc.build(elements)
    buffer.seek(0)
    response.write(buffer.read())
    
    return response

@login_required
def export_to_email(request):
    user = request.user
    expenses = Expense.objects.filter(user=user)
    income = Income.objects.filter(user=user)

    total_expense = expenses.aggregate(total_expense=Sum('amount'))['total_expense'] or 0
    total_income = income.aggregate(total_income=Sum('amount'))['total_income'] or 0
    balance = total_income - total_expense

    # Create PDF
    pdf_buffer = BytesIO()
    pdf_doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    pdf_elements = []

    # Add Expense Data to PDF
    pdf_data_expenses = [['Title', 'Amount', 'Date', 'Category', 'Description']]
    for expense in expenses:
        pdf_data_expenses.append([expense.title, expense.amount, expense.date, expense.category, expense.description])

    pdf_table_expenses = Table(pdf_data_expenses)
    pdf_table_expenses.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), '#d5d5d5'),
        ('TEXTCOLOR', (0, 0), (-1, 0), '#000000'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), '#f5f5f5'),
        ('GRID', (0, 0), (-1, -1), 1, '#000000'),
    ]))
    pdf_elements.append(pdf_table_expenses)

    # Add Income Data to PDF
    pdf_data_income = [['Title', 'Amount', 'Date', 'Source', 'Description']]
    for income_item in income:
        pdf_data_income.append([income_item.title, income_item.amount, income_item.date, income_item.source, income_item.description])

    pdf_table_income = Table(pdf_data_income)
    pdf_table_income.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), '#d5d5d5'),
        ('TEXTCOLOR', (0, 0), (-1, 0), '#000000'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), '#f5f5f5'),
        ('GRID', (0, 0), (-1, -1), 1, '#000000'),
    ]))
    pdf_elements.append(pdf_table_income)

    pdf_doc.build(pdf_elements)
    pdf_buffer.seek(0)

    # Create Excel
    excel_buffer = BytesIO()
    excel_workbook = xlsxwriter.Workbook(excel_buffer, {'in_memory': True})
    excel_worksheet_expenses = excel_workbook.add_worksheet('Expenses')
    excel_worksheet_income = excel_workbook.add_worksheet('Income')

    # Write Expense Data to Excel
    columns = ['Title', 'Amount', 'Date', 'Category', 'Description']
    for col_num, header in enumerate(columns):
        excel_worksheet_expenses.write(0, col_num, header)
    for row_num, expense in enumerate(expenses, 1):
        excel_worksheet_expenses.write(row_num, 0, expense.title)
        excel_worksheet_expenses.write(row_num, 1, expense.amount)
        excel_worksheet_expenses.write(row_num, 2, expense.date.strftime('%Y-%m-%d'))
        excel_worksheet_expenses.write(row_num, 3, expense.category)
        excel_worksheet_expenses.write(row_num, 4, expense.description)

    # Write Income Data to Excel
    columns_income = ['Title', 'Amount', 'Date', 'Source', 'Description']
    for col_num, header in enumerate(columns_income):
        excel_worksheet_income.write(0, col_num, header)
    for row_num, income_item in enumerate(income, 1):
        excel_worksheet_income.write(row_num, 0, income_item.title)
        excel_worksheet_income.write(row_num, 1, income_item.amount)
        excel_worksheet_income.write(row_num, 2, income_item.date.strftime('%Y-%m-%d'))
        excel_worksheet_income.write(row_num, 3, income_item.source)
        excel_worksheet_income.write(row_num, 4, income_item.description)

    excel_workbook.close()
    excel_buffer.seek(0)

    # Create email
    email = EmailMessage(
        subject='Your Financial Summary',
        body=f'Attached are your financial summaries as PDF and Excel files.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    
    # Attach PDF
    email.attach('financial_summary.pdf', pdf_buffer.read(), 'application/pdf')
    
    # Attach Excel
    email.attach('financial_summary.xlsx', excel_buffer.read(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    
    email.send()

    messages.success(request, 'Your financial summary has been sent to your email with attachments.')
    return redirect('expense_list')

from django.shortcuts import render
from django.db.models import Sum, F
from .models import Income, Expense

from django.shortcuts import render
from django.db.models import Sum, F
from .models import Income, Expense
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns
def dashboard_view2(request):
    user = request.user
    
    income_by_source = Income.objects.filter(user=user).values('source').annotate(total=Sum('amount'))
    expense_by_category = Expense.objects.filter(user=user).values('category').annotate(total=Sum('amount'))

    income_expense_by_date = (
        Expense.objects.filter(user=user)
        .values('date')
        .annotate(amount=Sum('amount'))
        .union(
            Income.objects.filter(user=user)
            .values('date')
            .annotate(amount=Sum(F('amount'))),
            all=True
        )
        .order_by('date')
    )
    
    dates = []
    balances = []
    balance = 0
    for entry in income_expense_by_date:
        balance += entry['amount']
        dates.append(entry['date'].strftime('%Y-%m-%d'))  # Ensure date is formatted as a string
        balances.append(balance)

    context = {
        'income_by_source': income_by_source,
        'expense_by_category': expense_by_category,
        'dates': dates,
        'balances': balances,
    }
    
    return render(request, 'expenses/dashboard2.html', context)

import matplotlib.pyplot as plt
import seaborn as sns
from django.shortcuts import render
from io import BytesIO
from django.http import HttpResponse
from .models import Expense, Income
from django.db.models import Sum

@login_required
def income_expense_dashboard(request):
    # Get data
    expenses = Expense.objects.filter(user=request.user)
    incomes = Income.objects.filter(user=request.user)

    # Calculate total income and expenses
    total_income = incomes.aggregate(total_income=Sum('amount'))['total_income'] or 0
    total_expense = expenses.aggregate(total_expense=Sum('amount'))['total_expense'] or 0
    balance = total_income - total_expense

    # Generate data for the balance trend line
    income_data = incomes.values('date').annotate(total=Sum('amount')).order_by('date')
    expense_data = expenses.values('date').annotate(total=Sum('amount')).order_by('date')

    income_dates = [entry['date'] for entry in income_data]
    income_totals = [entry['total'] for entry in income_data]

    expense_dates = [entry['date'] for entry in expense_data]
    expense_totals = [entry['total'] for entry in expense_data]

    # Plot data
    plt.figure(figsize=(10, 6))
    sns.lineplot(x=income_dates, y=income_totals, label='Income')
    sns.lineplot(x=expense_dates, y=expense_totals, label='Expenses')
    plt.xlabel('Date')
    plt.ylabel('Amount')
    plt.title('Balance Trend')
    plt.legend()
    plt.grid(True)

    # Save plot to buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')

    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'balance_trend_chart': img_str
    }

    return render(request, 'expenses/income_expense_dashboard.html', context)