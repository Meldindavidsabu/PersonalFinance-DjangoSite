import requests
from django.shortcuts import render
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')

def get_supported_currencies():
    """
    Fetch the list of supported currencies from the API and return as a dictionary.
    If the API fails, return an empty dictionary and handle error cases gracefully.
    """
    url = "https://currency-converter5.p.rapidapi.com/currency/list"
    
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "currency-converter5.p.rapidapi.com"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Will raise HTTPError for bad responses (4xx or 5xx)
        currencies = response.json().get("currencies", {})
        return currencies
    except requests.exceptions.RequestException as e:
        print(f"Error fetching supported currencies: {e}")
        return {}

def convert_currency(request):
    """
    Handle both GET and POST requests for the currency converter.
    On POST, it fetches the conversion rate and displays the result.
    On GET, it simply renders the form with currency options.
    """
    currency_choices = get_supported_currencies()

    if request.method == 'POST':
        from_currency = request.POST.get('from_currency')
        to_currency = request.POST.get('to_currency')
        amount = request.POST.get('amount', 1)

        if not from_currency or not to_currency or not amount:
            return render(request, 'currency/currency_converter.html', {
                'error': 'Please provide valid input for all fields.',
                'currency_choices': currency_choices
            })

        url = f"https://currency-converter5.p.rapidapi.com/currency/convert?format=json&from={from_currency}&to={to_currency}&amount={amount}"
        
        headers = {
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": "currency-converter5.p.rapidapi.com"
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            data = response.json()
            print("API Response:", data)  # Debugging print statement

            # Check if the 'rates' key and 'to_currency' are present in the response
            if 'rates' in data and to_currency in data['rates']:
                converted_amount = data['rates'][to_currency].get('rate_for_amount', 'N/A')
            else:
                converted_amount = 'N/A'

            return render(request, 'currency/currency_converter.html', {
                'converted_amount': converted_amount,
                'from_currency': from_currency,
                'to_currency': to_currency,
                'amount': amount,
                'currency_choices': currency_choices
            })
        except requests.exceptions.RequestException as e:
            print(f"Error during currency conversion: {e}")
            return render(request, 'currency/currency_converter.html', {
                'error': f'An error occurred while converting the currency: {e}. Please try again later.',
                'currency_choices': currency_choices
            })

    else:
        return render(request, 'currency/currency_converter.html', {
            'currency_choices': currency_choices
        })
