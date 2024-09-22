# Generated by Django 5.0.8 on 2024-09-11 08:01

import expenses.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0021_alter_expense_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[expenses.models.validate_positive], verbose_name='Expense Amount'),
        ),
    ]
