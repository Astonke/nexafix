from django.urls import path,include
from .views import default,pay,submit_payment_proof,add_code

urlpatterns = [
    path('', default,name='default_page'),
    path('go-pay/', pay,name='payment_page'),
    path('submit_payment_proof/', submit_payment_proof, name='submit_payment_proof'),
    path('vcode/<str:v_code>/', add_code,name='payment_page'),   
]