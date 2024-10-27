from django.urls import path
from .views import process_message, success_page, home

urlpatterns = [
    path('auth/', home, name='home'),
    path('submit/', process_message, name='submit_message'),
    path('page/<uuid:token>/', success_page, name='success_page'),
]
