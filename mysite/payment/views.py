from django.shortcuts import render

# Create your views here.
def default(request):
    return render(request,'mid_pay.html')

def pay(request):
    kes_amnt='130'
    amount={'amount':f'$1 / kes:{kes_amnt} equiv'}
    return render(request,'pay_home.html',context=amount)


from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages

def submit_payment_proof(request):
    if request.method == 'POST':
        proof_of_payment = request.POST.get('proof_of_payment')
        user_email = request.POST.get('email')
        mobile_number = request.POST.get('mobile_number')

        if proof_of_payment and user_email and mobile_number:
            # Send an email to the predefined email address
            send_mail(
                'Proof of Payment Submitted',
                f'Proof of Payment:\n{proof_of_payment}\n\nEmail: {user_email}\nMobile: {mobile_number}',
                'crashcoders6@gmail.com',  # Replace with your email
                ['crashcoders6@gmail.com'],  # Replace with your email
                fail_silently=False,
            )
            messages.success(request, "Payment proof submitted successfully!")
            #return redirect('payment_success')
        else:
            messages.error(request, "All fields are required.")

    return render(request, 'proof.html')

def payment_success(request):
    return render(request, 'payment_success.html')
