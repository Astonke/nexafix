from django.urls import path,include
from .views import default,pay,submit_payment_proof

urlpatterns = [
    path('', default,name='default_page'),
    path('go-pay/', pay,name='payment_page'),
    path('submit_payment_proof/', submit_payment_proof, name='submit_payment_proof'),

]