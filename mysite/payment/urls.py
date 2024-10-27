from django.urls import path,include
<<<<<<< HEAD
from .views import default,pay,submit_payment_proof,add_code
=======
from .views import default,pay,submit_payment_proof
>>>>>>> 3f78c95d4af5d6e6d885eda22a52f553fa7973a7

urlpatterns = [
    path('', default,name='default_page'),
    path('go-pay/', pay,name='payment_page'),
    path('submit_payment_proof/', submit_payment_proof, name='submit_payment_proof'),
    path('vcode/<str:v_code>/', add_code,name='payment_page'),   
]
