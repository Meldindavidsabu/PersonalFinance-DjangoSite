import requests
from django.shortcuts import render
from django.http import JsonResponse

def fetch_mutual_funds(request):
    # URL for the mutual fund API
    url = 'https://api.kuvera.in/mf/api/v4/fund_schemes/FRAG-GR%7CSBD028G-GR.json'
    headers = {'accept': 'application/json'}

    try:
        # Make a GET request to the API
        response = requests.get(url, headers=headers)
        # Check if the request was successful
        response.raise_for_status()
        # Parse the response JSON data
        data = response.json()

        # Debug print to verify response
        print("API Response:", data)
        
        # Ensure data is a list
        if isinstance(data, list):
            funds = data
        else:
            funds = []

        # Render the mutual funds page with the data
        return render(request, 'fund_integration/mutual_funds.html', {'funds': funds})

    except requests.RequestException as e:
        # Handle any request errors and return an error message
        return render(request, 'fund_integration/mutual_funds.html', {'error': str(e)})

def mutual_fund_api(request):
    # URL for the mutual fund API
    url = 'https://api.kuvera.in/mf/api/v4/fund_schemes/FRAG-GR%7CSBD028G-GR.json'
    headers = {'accept': 'application/json'}

    try:
        # Make a GET request to the API
        response = requests.get(url, headers=headers)
        # Check if the request was successful
        response.raise_for_status()
        # Parse the response JSON data
        data = response.json()

        # Return the data as JSON response
        return JsonResponse(data, safe=False)

    except requests.RequestException as e:
        # Handle any request errors and return an error message as JSON response
        return JsonResponse({'error': str(e)}, status=500)
