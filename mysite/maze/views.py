from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
# Suggested code may be subject to a license. Learn more: ~LicenseLog:390210754.
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .forms import ServiceProviderForm, ServiceProviderImageFormSet
from .models import Category, Service
from .forms import ServiceForm
from .models import SubCategory
from django.http import JsonResponse
from .funcs import verify_code

def upload_service(request):
    form = ServiceForm(request.POST, request.FILES)
    if request.method == 'POST':
        verif_code = request.POST.get('verif')
        #print(verif_code)
        if verify_code(verif_code):
            #form = ServiceForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your service has been uploaded successfully!')
                return redirect('/home')  # Redirect to the same page or another page"""
            else:
                form = ServiceForm()
        else:
            messages.error(request,'Invalid code')

    return render(request, 'upload_service.html', {'form': form})

from .models import PendingService  # Import the new PendingService model


def upload_await_verification(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            # Intercept and save the service data in PendingService model
            pending_service = PendingService(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                image=form.cleaned_data['image'],
                user=request.user  # Store the user who uploaded the service
            )
            pending_service.save()

            # Redirect to the payment page
            return redirect('payment_page', pending_service_id=pending_service.id)
    else:
        form = ServiceForm()

    return render(request, 'upload_service.html', {'form': form})

def load_subcategories(request):
    category_id = request.GET.get('category')
    subcategories = SubCategory.objects.filter(category_id=category_id).order_by('name')
    return JsonResponse(list(subcategories.values('id', 'name')), safe=False)



def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    return render(request, 'service_detail.html', {'service': service})

def category_services(request, category_str):
    # Get the category by name (case-insensitive)
    category = get_object_or_404(Category, name__iexact=category_str)

    # Fetch services that belong to this category
    services = Service.objects.filter(subcategory__category=category)

    return render(request, 'category_services.html', {'category': category, 'services': services})

from .forms import ServiceForm, SearchForm

from django.db import models

def home_def(request):
    # Fetch all categories
    categories = Category.objects.all()
    return render(request, 'def2.html', {'categories': categories})

from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Service

def search_services(request):
    query = request.GET.get('q')  # Get the search query from the request
    if query:
        services = Service.objects.filter(title__icontains=query)  # Adjust filter as needed
        # Order the services by title (or any other field you prefer)
        services = services.order_by('title')  # Explicitly order the services
    else:
        services = Service.objects.none()  # Return an empty QuerySet if no query

    # Paginate the results
    paginator = Paginator(services, 9)  # Show 9 services per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'search_results.html', {
        'query': query,
        'services': page_obj,  # Pass the page object to the template
    })


#@csrf_exempt
def login_register(request):
    if request.method == 'POST':
        if 'login' in request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('/homez')  # Replace with your desired redirect URL
            else:
                messages.error(request, 'Invalid username or password.')
        elif 'register' in request.POST:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            if password == confirm_password:
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Username already taken.')
                elif User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already in use.')
                else:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()
                    messages.success(request, 'Account created successfully!')
                    return redirect('home')  # Replace with your desired redirect URL
            else:
                messages.error(request, 'Passwords do not match.')

    return render(request, 'accounts/login_register.html')

def home(request):
    return render(request, 'home3.html')

def logout(request):
    auth_logout(request)
    return redirect('login_register')

from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from .models import ServiceProvider

def log_click(request, provider_id):
    provider = ServiceProvider.objects.get(id=provider_id)
    provider.clicks += 1
    provider.save()
    return JsonResponse({'status': 'success'})

"""
def service_providers(request):
    providers = ServiceProvider.objects.all().order_by('-clicks', '-impressions')
    return render(request, 'home3.html', {'providers': providers})"""
from .models import Service

def service_providers(request):
    # Fetch services ordered by creation time
    services = Service.objects.all().order_by('-created_at')

    # Render the page and pass services as 'providers'
    return render(request, 'home3.html', {'providers': services})


from django.http import Http404, FileResponse
from django.views import View



class ServiceFileView(View):
    def get(self, request, service_id):
        try:
            service = Service.objects.get(id=service_id)
            if service.file:
                # Open the file and return it without attachment
                return FileResponse(service.file.open(), content_type='application/pdf')  # Adjust content type as needed
            else:
                raise Http404("File not found.")
        except Service.DoesNotExist:
            raise Http404("Service does not exist.")


@csrf_exempt
def add_service_provider(request):
    if request.method == 'POST':
        form = ServiceProviderForm(request.POST)
        formset = ServiceProviderImageFormSet(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid():
            service_provider = form.save()
            images = formset.save(commit=False)
            for image in images:
                image.service_provider = service_provider
                image.save()
            return redirect('service_providers')  # Adjust this to your actual view name
    else:
        form = ServiceProviderForm()
        formset = ServiceProviderImageFormSet()

    return render(request, 'adder3.html', {'form': form, 'formset': formset})

from .models import Service, SubCategory  # Adjust import as necessary

def services_by_category(request, category_id):
    # Fetch the subcategory object
    subcategory = get_object_or_404(SubCategory, id=category_id)

    # Get services related to the subcategory and order them
    services = Service.objects.filter(subcategory=subcategory).order_by('-created_at')  # Change order as needed

    # Implement pagination
    paginator = Paginator(services, 10)  # Show 10 services per page
    page_number = request.GET.get('page')
    services_page = paginator.get_page(page_number)

    # Render the template with the services
    return render(request, 'your_template.html', {'services': services_page, 'subcategory': subcategory})

from django.http import JsonResponse
from .models import Service, PendingService

@csrf_exempt
def verify_payment(request, pending_service_id):
    if request.method == 'POST':
        # Fetch the pending service
        pending_service = PendingService.objects.get(id=pending_service_id)

        # Check the payment verification (this is just a mock, you'd integrate PayPal's SDK here)
        # Assuming payment verification is successful...
        if True:  # Replace this condition with actual verification logic
            # Create the actual Service entry from the pending service data
            new_service = Service.objects.create(
                title=pending_service.title,
                description=pending_service.description,
                image=pending_service.image,
                user=pending_service.user
            )

            # Mark pending service as verified or delete it if not needed
            pending_service.is_verified = True
            pending_service.save()

            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'failed'}, status=400)


def upload_success(request):
    return render(request, 'upload_success.html')

from django.urls import reverse
from django.shortcuts import redirect

from encron.tools import find_file
def payment_page(request, pending_service_id):
    # Retrieve the pending service using the provided ID
    pending_service = get_object_or_404(PendingService, id=pending_service_id)

    # Process the payment for the pending service
    return render(request, 'payment_page.html', {'pending_service': pending_service})


#about page
def about(request):
    return render(request,'about_nexa.html')

#contact-details
def contact_detail(request):
    return render(request,'contact_details.html')

def why_pay(request):
    return render(request,'pay_about.html')
