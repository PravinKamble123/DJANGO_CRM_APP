from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import SignupForm, LoginForm


from .models import Userprofile 

from team.models import Team
from .models import Userprofile



def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # log the user in
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'user/signup.html', {'form': form})

            
            
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # Log the user in
            user = form.get_user()
            login(request, user)
            return redirect('index')  # Replace 'home' with your desired URL name
    else:
        form = AuthenticationForm()
    return render(request, 'user/login.html', {'form': form})

@login_required
def my_account(request):
    team= Team.objects.filter(created_by=request.user)
    if team.exists():
        team = team.first()
    else:
        team = None
    
    return render(request,'user/myaccount.html',{
        'team':team
    })
