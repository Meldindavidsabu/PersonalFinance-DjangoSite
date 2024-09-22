from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Due
from .forms import DueForm
from django.core.mail import send_mail
from django.db.models import Sum
from django.utils import timezone
from django.db.models import F

@login_required
@login_required

@login_required
def dashboard(request):
    dues = Due.objects.filter(user=request.user)  # Filter by logged-in user
    for due in dues:
        days_remaining = due.days_remaining()  # Call the method with parentheses
        if days_remaining == 0:
            due.bg_class = 'bg-danger'
        elif days_remaining <= 3:
            due.bg_class = 'bg-warning'
        else:
            due.bg_class = 'bg-info'
        due.progress_width = 100 - days_remaining  # Add this line

    context = {
        'dues': dues
    }
    return render(request, 'dashboard.html', context)
@login_required
def due_list(request):
    # Retrieve filters from GET parameters
    amount_filter = request.GET.get('amount')
    person_entity_filter = request.GET.get('person_entity')
    borrowed_on_filter = request.GET.get('borrowed_on')
    return_date_filter = request.GET.get('return_date')
    reason_filter = request.GET.get('reason')
    
    # Start with all dues for the logged-in user
    dues = Due.objects.filter(user=request.user)
    
    # Apply filters
    if amount_filter:
        dues = dues.filter(amount__icontains=amount_filter)
    if person_entity_filter:
        dues = dues.filter(person_entity__icontains=person_entity_filter)
    if borrowed_on_filter:
        dues = dues.filter(borrowed_on=borrowed_on_filter)
    if return_date_filter:
        dues = dues.filter(return_date=return_date_filter)
    if reason_filter:
        dues = dues.filter(reason__icontains=reason_filter)
    
    # Calculate total amount
    total_amount = dues.aggregate(total_amount=Sum('amount'))['total_amount'] or 0

    context = {
        'dues': dues,
        'total_amount': total_amount,
    }
    return render(request, 'due_list.html', context)

@login_required
def add_due(request):
    if request.method == 'POST':
        form = DueForm(request.POST)
        if form.is_valid():
            due = form.save(commit=False)
            due.user = request.user
            due.save()
            return redirect('due_list')
    else:
        form = DueForm()
    return render(request, 'add_due.html', {'form': form})

@login_required
def edit_due(request, due_id):
    due = get_object_or_404(Due, id=due_id, user=request.user)
    if request.method == 'POST':
        form = DueForm(request.POST, instance=due)
        if form.is_valid():
            form.save()
            return redirect('due_list')
    else:
        form = DueForm(instance=due)
    return render(request, 'edit_due.html', {'form': form})

@login_required
def delete_due(request, due_id):
    due = get_object_or_404(Due, id=due_id, user=request.user)
    if request.method == 'POST':
        due.delete()
        return redirect('due_list')
    return render(request, 'delete_due.html', {'due': due})

@login_required
def notify_due(request, due_id):
    due = get_object_or_404(Due, id=due_id, user=request.user)
    if request.method == 'POST':
        borrower_email = request.POST.get('borrower_email')
        due.send_due_reminder(borrower_email)
        return redirect('due_list')
    return redirect('due_list')

def filter_dues(request):
    # Retrieve filter parameters from GET request
    amount = request.GET.get('amount', '')
    person_entity = request.GET.get('person_entity', '')
    borrowed_on = request.GET.get('borrowed_on', '')
    return_date = request.GET.get('return_date', '')
    reason = request.GET.get('reason', '')

    # Filter the Dues based on the provided parameters for the logged-in user
    dues = Due.objects.filter(user=request.user)
    if amount:
        dues = dues.filter(amount=amount)
    if person_entity:
        dues = dues.filter(person_entity__icontains=person_entity)
    if borrowed_on:
        dues = dues.filter(borrowed_on=borrowed_on)
    if return_date:
        dues = dues.filter(return_date=return_date)
    if reason:
        dues = dues.filter(reason__icontains=reason)

    # Calculate the total amount of filtered dues
    total_amount = dues.aggregate(total=Sum('amount'))['total'] or 0

    # Render the template with filtered dues and total amount
    return render(request, 'due_list.html', {'dues': dues, 'total_amount': total_amount})
from django import template

register = template.Library()

@register.filter
def add_class(value, arg):
    return value.as_widget(attrs={'class': arg})
