
from django.contrib import admin
from django.urls import path, include
from data.views import data_dashboard  # Import your existing view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('data/', include('data.urls')),
    path('', data_dashboard, name='home'),  # Add this line for the root URL
]
