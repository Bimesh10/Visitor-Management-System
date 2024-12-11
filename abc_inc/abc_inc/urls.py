# abc_inc/urls.py

from django.contrib import admin
from django.urls import path, include  # Use include to route to app URLs

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('visitors.urls')),  # Includes app URLs from the 'visitors' app
]
