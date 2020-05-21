from django.urls import path
from teste_app import views

urlpatterns = [
    path('', views.checkout_view,name='checkout'),
    path('webhook', views.webhook,name='webhook'),
]
