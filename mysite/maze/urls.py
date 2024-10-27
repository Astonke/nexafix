from django.urls import path
from .views import login_register, service_providers, logout
from maze import views
from maze import mail
from .views import upload_service, load_subcategories
from .views import ServiceFileView, category_services, service_detail  # Import the new service_detail view

urlpatterns = [
    path('login_register/', login_register, name='login_register'),
    path('auth/', login_register, name='login_register'),  # Ensure trailing slash consistency
    path('home/', service_providers, name='home'),
    path('logout/', logout, name='logout'),
    path('', views.service_providers, name='service_providers'),
    path('test-mail/', mail.send_test_email, name='test-mail'),
    path('homez/', views.home_def, name='service_page'),  # Added trailing slash for consistency
    path('upload_service/', views.upload_service, name='upload_service'),  # Added trailing slash for consistency
    path('category/<str:category_str>/', views.category_services, name='category_services'),  # This is for categories
    path('search/', views.search_services, name='search'),
    path('contact/', mail.contact, name='contact'),
    #path('upload/', upload_service, name='upload_service'),
    path('ajax/load-subcategories/', load_subcategories, name='ajax_load_subcategories'),
    path('services/<int:service_id>/', ServiceFileView.as_view(), name='service-file'),
    path('service/<int:service_id>/', service_detail, name='service_detail'),  # New URL pattern for service detail

    path('payment/<int:pending_service_id>/', views.payment_page, name='payment_page'),
    path('verify-payment/<int:pending_service_id>/', views.verify_payment, name='verify_payment'),
    path('upload-success/', views.upload_success, name='upload_success'),

    path('about/', views.about, name='about'),
    path('contact-nexa/', views.contact_detail, name='about'),
   
]
