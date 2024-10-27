from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import MpesaTransaction
from .forms import MpesaMessageForm
import re

def home(request):
    return render(request, 'submit_msg.html')

def extract_transaction_details(message):
    # Simple regex patterns to extract M-Pesa details
    transaction_id_pattern = r"Transaction ID:\s*(\w+)"
    amount_pattern = r"Amount:\s*([0-9]+\.?[0-9]*)"
    receiver_pattern = r"Receiver:\s*(\w+)"
    time_pattern = r"Time:\s*(\d{4}-\d{2}-\d{2} \d{2}:\d{2})"
    phone_number_pattern = r"Phone Number:\s*(\+?\d+)"

    # Extract details
    transaction_id = re.search(transaction_id_pattern, message)
    amount = re.search(amount_pattern, message)
    receiver = re.search(sender_pattern, message)
    time = re.search(time_pattern, message)
    phone_number = re.search(phone_number_pattern, message)

    if transaction_id and amount and sender and time and phone_number:
        return {
            'transaction_id': transaction_id.group(1),
            'amount': float(amount.group(1)),
            'receiver': receiver.group(1),
            'time': time.group(1),
            'phone_number': phone_number.group(1),
        }
    return None

def validate_transaction(transaction_details):
    # Check if transaction ID has already been used
    if MpesaTransaction.objects.filter(transaction_id=transaction_details['transaction_id']).exists():
        return False

    # Additional checks can be added here (e.g., time validity)
    return True

def success_page(request, token):
    try:
        transaction = MpesaTransaction.objects.get(token=token)
        if transaction.is_valid:
            return render(request, 'success_msg.html', {'transaction': transaction})
    except MpesaTransaction.DoesNotExist:
        return HttpResponse('Invalid token.', status=404)


def process_message(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        fox = request.POST.get('fox')
        print(message)
        print(fox)
        return redirect('home')
    else:
        return HttpResponse('reload', status=200)

