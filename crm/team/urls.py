from django.urls import path

from .views import *

app_name='team'

urlpatterns = [
    path('<int:pk>/', detail, name='detail'),
    path('<int:pk>/edit/', edit_team, name='edit_team'),
    
]