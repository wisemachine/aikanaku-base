
from django.shortcuts import render
from .models import DataInformation

def data_dashboard(request):
    data_info = DataInformation.objects.all()
    return render(request, 'dashboard.html', {'data_info': data_info})
