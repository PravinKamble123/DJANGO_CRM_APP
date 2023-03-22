from django.urls import path
from .views import *

app_name = 'lead'

urlpatterns = [
    path('', LeadListView.as_view(), name='lead_list'),
    path('add_lead/', add_lead, name='add_lead'),
    path('<int:pk>/', lead_detail, name='lead_detail'),
    path('<int:pk>/delete/', leads_delete, name='lead_delete'),
    path('<int:pk>/edit/', leads_edit, name='leads_edit'),
    path('<int:pk>/convert/', convert_to_client, name='convert_to_client'),
    path('<int:pk>/add-comment', add_comment, name='add_comment'),
]
