from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from lead.models import Lead
from client.models import Client
from team.models import Team

@login_required
def dashboard(request):
    team = Team.objects.filter(created_by=request.user)
    if team.exists():
        team = team.first()
    else:
        team = None
    leads = Lead.objects.filter( created_by=request.user,team=team, converted_to_client=False).order_by('-created_at')[0:5]
    clients = Client.objects.filter(created_by=request.user,team=team).order_by('-created_at')[0:5]
    return render(request,'dashboard/dashboard.html',{
        'leads':leads,
        'clients':clients,
        'team':team
    })
