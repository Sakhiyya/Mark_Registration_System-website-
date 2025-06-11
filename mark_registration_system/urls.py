from django.urls import path
from . import views  # Import views from the current app

urlpatterns = [
    path('', views.home, name='home'),  # Home page path
    path('input-marks/', views.input_marks, name='input_marks'),
    path('view-marks/', views.view_marks, name='view_marks'),
    path('update-marks/', views.update_marks, name='update_marks'),
    path('visualization/', views.visualization, name='visualization'),
]
