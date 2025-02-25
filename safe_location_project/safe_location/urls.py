from django.contrib import admin
from django.urls import path, include
from risk_data.views import home  # Import the home view

urlpatterns = [
    path('', home, name='home'),  # Add this line for the homepage
    path('admin/', admin.site.urls),
    path('risk/', include('risk_data.urls')),
]
