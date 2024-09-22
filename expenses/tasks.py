# expenses/tasks.py
from celery import shared_task
from django.core.mail import EmailMessage
from .models import Expense, Income
from django.contrib.auth.models import User

@shared_task
def send_weekly_summary():
    users = User.objects.all()
    for user in users:
        expenses = Expense.objects.filter(user=user)
        incomes = Income.objects.filter(user=user)

        subject = "Your Weekly Financial Summary"
        body = "Here is your financial summary for the past week:\n\n"

        body += "Expenses:\n"
        for expense in expenses:
            body += f"{expense.date}: {expense.category} - {expense.amount}\n"

        body += "\nIncomes:\n"
        for income in incomes:
            body += f"{income.date}: {income.category} - {income.amount}\n"

        body += f"\nBalance: {sum(income.amount for income in incomes) - sum(expense.amount for expense in expenses)}"

        email = EmailMessage(subject, body, to=[user.email])
        email.send()
