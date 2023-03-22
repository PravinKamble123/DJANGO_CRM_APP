from django.views import View
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .forms import AddLeadForm, AddCommentForm, AddFileForm
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required
from .models import Comment, Lead
from client.models import Client, Comment as clientcomment
from team.models import Team
from django.views.generic import ListView, DetailView, DeleteView
from django.utils.decorators import method_decorator





class LeadListView(LoginRequiredMixin, ListView):
    model = Lead
    template_name = 'lead/lead_list.html'
    context_object_name = 'leads'
    paginate_by = 10
    
    def get_queryset(self):
        return self.model.objects.filter(created_by=self.request.user, converted_to_client=False)


    
@login_required
def lead_detail(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    comments = Comment.objects.filter(lead=lead)
    form1 = AddFileForm()
    form2 = AddCommentForm()
    context = {
        'lead': lead,
        'comments': comments,
        'form1':form1,
        'form2':form2
    }
    return render(request, 'lead/lead_detail.html', context)


@login_required
def leads_delete(request, pk):
    lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
    lead.delete()
    messages.success(request, 'The lead deleted successfully!')
    return redirect('lead:lead_list')


@login_required
def leads_edit(request,pk):
    print('leads_edit view called') 
    lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
    if request.method == 'POST':
        print('POST request received')
        form = AddLeadForm(request.POST, instance=lead)

        if form.is_valid():
            form.save()
        
        messages.success(request, 'Lead updated successfully!')

        return redirect('lead:lead_list')
    
    else:
        print('GET request received')
        form=AddLeadForm(instance=lead)
    
    return render(request, 'lead/leads_edit.html',{
        "form":form
    })
@login_required
def add_lead(request):
    teams = Team.objects.filter(created_by=request.user)
    if teams.exists():
        team = teams.first()
    else:
        team = None
    if request.method == 'POST':
        form = AddLeadForm(request.POST)
        if form.is_valid():
            lead = form.save(commit=False)
            lead.created_by = request.user
            lead.team = team
            lead.save()

            messages.success(request, 'The lead added successfully!')

            return redirect('lead:lead_list')
    else:
        form_initial = {}
        if team:
            form_initial['team'] = team.id
        form = AddLeadForm(initial=form_initial)

    return render(request, 'lead/add_lead.html',{
        "form":form,
        "team":team
    })



@login_required
def convert_to_client(request, pk):
    lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
    teams = Team.objects.filter(created_by=request.user)
    if teams.exists():
        team = teams.first()
    else:
        team = None

    client = Client.objects.create(
        name=lead.name,
        email=lead.email,
        description=lead.description,
        created_by=request.user,
        team=team,
    )

    lead.converted_to_client=True
    lead.save()

    # convert lead comments to clients comments
    comments = lead.comments.all()
    
    for comment in comments:
        clientcomment.objects.create(
            client = client,
            content = comment.content,
            created_by = comment.created_by,
            team = team

        )
    
    # show message and redirect

    messages.success(request, 'The lead converted to a client successfully!')
    return redirect('lead:lead_list')


@login_required
def add_comment(request, pk):
    lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
    teams = Team.objects.filter(created_by=request.user)
    if teams.exists():
        team = teams.first()
    else:
        team = None
    if request.method == 'POST':
        form = AddCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.created_by = request.user
            comment.team = team
            comment.lead = lead
            comment.save()

            messages.success(request, 'The comment added successfully!')

            return redirect('lead:lead_detail', pk=pk)
    else:
        form_initial = {}
        if team:
            form_initial['team'] = team.id
        form = AddCommentForm(initial=form_initial)

    return render(request, 'lead/add_comment.html', {
        "form": form,
        "team": team,
    })


