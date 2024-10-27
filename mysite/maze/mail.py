# views.py

from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect,get_object_or_404


from .forms import ContactForm
from django.contrib import messages

def contact(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        message = request.POST.get('message')

        # Send email logic
        send_mail(
            'New Contact Form Submission',
            f'Email: {email}\nPhone: {phone_number}\nMessage: {message}',
            'crashcoders6@gmail.com',  # Replace with your email
            ['crashcoders6@gmail.com'],  # Replace with the recipient's email
        )

        messages.success(request, 'Your message has been sent successfully!')
        return render(request, 'contact.html')

    return render(request, 'contact.html')

def send_test_email(request):
    subject = 'Test Email'
    message = 'need to report technician!'
    recipient_list = ['crashcoders6@gmail.com']  # Add recipients
    from_email = settings.DEFAULT_FROM_EMAIL
    
    # Sending email
    send_mail(subject, message, from_email, recipient_list)
    
    return HttpResponse('Email sent successfully!')

#send_test_email('hay')

def send_html_email(request):
    subject = 'HTML Email'
    html_content = '<h1>Hello</h1><p>This is an HTML email!</p>'
    from_email = 'your-email@gmail.com'
    recipient_list = ['recipient@example.com']

    # Create EmailMessage object
    email = EmailMessage(subject, html_content, from_email, recipient_list)
    email.content_subtype = 'html'  # Specify the email content is HTML
    
    # Send email
    email.send()

    return HttpResponse('HTML Email sent successfully!')

