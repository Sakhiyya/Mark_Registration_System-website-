from django.contrib import admin
from django.urls import path, include  # Include function to reference app-level URLs
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mark_registration_system.urls')),  # Include app-level URLs
]

urlpatterns += staticfiles_urlpatterns()
