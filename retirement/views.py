from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import RetirementGoalForm
from .models import RetirementGoal
import requests

API_KEY = '579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b'

def get_india_inflation_rate():
    url = 'https://api.data.gov.in/resource/352b3616-9d3d-42e5-80af-7d21a2a53fab'
    params = {
        'api-key': API_KEY,
        'format': 'json',
        'limit': 1,  # Fetch the latest record
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()  # Attempt to parse JSON

        # Extracting the latest inflation rate (CPI-C Inflation %)
        records = data.get('records', [])
        if records:
            latest_record = records[0]
            inflation_rate = latest_record.get('cpi_c_inflation_', 'N/A')  # Use .get() to avoid KeyError
        else:
            inflation_rate = 'N/A'  # Handle case where no records are returned

    except requests.RequestException as e:
        # Handle network-related errors
        print(f"Request failed: {e}")
        inflation_rate = 'N/A'  # Default value in case of error

    return inflation_rate

# View to create a new retirement goal
@login_required
def create_goal(request):
    inflation_rate = get_india_inflation_rate()  # Fetch inflation rate

    if request.method == 'POST':
        form = RetirementGoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user  # Ensure goal is linked to the logged-in user
            goal.save()
            return redirect('goal_list')
    else:
        form = RetirementGoalForm()

    return render(request, 'retirement/create_goal.html', {
        'form': form,
        'inflation_rate': inflation_rate,
    })

# View to list retirement goals of the logged-in user
@login_required
def goal_list(request):
    goals = RetirementGoal.objects.filter(user=request.user)
    inflation_rate = get_india_inflation_rate()  # Fetch inflation rate
    return render(request, 'retirement/goal_list.html', {
        'goals': goals,
        'inflation_rate': inflation_rate
    })

# View to edit an existing retirement goal
@login_required
def edit_goal(request, id):
    goal = get_object_or_404(RetirementGoal, id=id, user=request.user)  # Ensure only user's goals can be edited
    if request.method == 'POST':
        form = RetirementGoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            return redirect('goal_list')
    else:
        form = RetirementGoalForm(instance=goal)
    return render(request, 'retirement/edit_goal.html', {'form': form, 'goal': goal})

# View to delete a retirement goal
@login_required
def delete_goal(request, id):
    goal = get_object_or_404(RetirementGoal, id=id, user=request.user)  # Ensure only user's goals can be deleted
    if request.method == 'POST':
        goal.delete()
        return redirect('goal_list')

    return render(request, 'retirement/goal_confirm_delete.html', {'goal': goal})

# View to display retirement goals chart
@login_required
def chart_view(request):
    user_goals = RetirementGoal.objects.filter(user=request.user)
    inflation_rate = get_india_inflation_rate()  # Fetch inflation rate

    # Prepare data for the template
    goals = []
    for goal in user_goals:
        goals.append({
            'goal_name': goal.goal_name,
            'target_amount': goal.target_amount,
            'current_amount': goal.current_amount,
            'progress_percentage': goal.progress_percentage(),  # Assuming this method returns a percentage
        })

    context = {
        'goals': goals,
        'inflation_rate': inflation_rate,
    }
    
    return render(request, 'retirement/retirement_goals_chart.html', context)

# View to list all retirement goals (not recommended if you want to restrict to user-specific goals)
@login_required
def retirement_goal_list(request):
    goals = RetirementGoal.objects.filter(user=request.user)  # Updated to filter by user
    return render(request, 'retirement/goal_list.html', {'goals': goals})
