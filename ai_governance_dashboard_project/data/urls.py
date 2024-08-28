
from django.urls import path
from .views import data_dashboard

urlpatterns = [
    path('dashboard/', data_dashboard, name='data_dashboard'),
]
