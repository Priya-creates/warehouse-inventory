from django.contrib import admin
from django.urls import path, include  # ← include must be imported

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inventory.urls')),  # ← THIS line must live here
]
