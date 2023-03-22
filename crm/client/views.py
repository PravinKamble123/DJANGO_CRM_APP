import csv

from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from .forms import AddClientForm, AddCommentForm
from django.contrib.auth.decorators import login_required

from .models import Client
from team.models import Team


@login_required
def client_export(request):
    clients = Client.objects.filter(created_by= request.user)

    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="clients.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(['Clients','Description','Created at','Crreated by'])

    for client in clients:
        writer.writerow([f"{client.name}", f"{client.description}", f"{client.created_at}", f"{client.created_by}"])
    
    return response


@login_required
def client_list(request):
    clients = Client.objects.filter(created_by= request.user,)

    return render(request,'client/client_list.html',{
        'clients': clients 
    })

@login_required
def client_detail(request, pk):
    client = get_object_or_404(Client, created_by=request.user, pk=pk)
    teams = Team.objects.filter(created_by=request.user)
    if teams.exists():
        team = teams.first()
    else:
        team = None

    if request.method == 'POST':
        form = AddCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.team = team 
            comment.created_by = request.user
            comment.client = client
            comment.lead = client
            print(comment.client)
            comment.save()
            return redirect('client:client_detail', pk=pk)
    else:
        form = AddCommentForm()

    return render(request,'client/client_detail.html',{
        'client': client,
        'form': form,  # add form to template context
    })


@login_required
def client_delete(request, pk):
    client = get_object_or_404(Client, created_by=request.user, pk=pk)
    client.delete()
    messages.success(request, 'The lead deleted successfully!')
    return redirect('client:client_list')


@login_required
def client_edit(request,pk):
    print('client_edit view called') 
    client = get_object_or_404(Client, created_by=request.user, pk=pk)
    if request.method == 'POST':
        print('POST request received')
        form = AddClientForm(request.POST, instance=client)

        if form.is_valid():
            form.save()
        
        messages.success(request, 'client details updated successfully!')

        return redirect('client:client_list')
    
    else:
        print('GET request received')
        form=AddClientForm(instance=client)
    
    return render(request, 'client/client_edit.html',{
        "form":form
    })

@login_required
def add_client(request):
    teams = Team.objects.filter(created_by=request.user)
    if teams.exists():
        team = teams.first()
    else:
        team = None
    if request.method == 'POST':
        form = AddClientForm(request.POST)
        team = Team.objects.filter(created_by=request.user)[0]

        if form.is_valid():
            client = form.save(commit=False)
            client.created_by = request.user
            client.team=team
            client.save()

            messages.success(request, 'The client added successfully!')

            return redirect('client:client_list')
    
    else:
        form = AddClientForm()



    return render(request, 'client/add_client.html',{
        "form":form,
        "team":team
    })

