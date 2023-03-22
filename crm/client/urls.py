from django.urls import path

from .views import *

app_name = 'client'

urlpatterns = [
    path('', client_list, name='client_list'),
    path('<int:pk>/', client_detail, name='client_detail'),
    path('<int:pk>/delete/', client_delete, name='client_delete'),
    path('<int:pk>/edit/', client_edit, name='client_edit'),
    path('<int:pk>/add-comment/', client_detail, name='add_comment'),
    path('add/', add_client, name='add_client'),
    path('export/',client_export,name='client_export'),
]
