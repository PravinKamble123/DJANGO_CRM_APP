from django.urls import path
from django.contrib.auth import views
from .views import signup, my_account

app_name = 'user'

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('myaccount/', my_account, name='my_account'),
    path('login/', views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]
