from django.shortcuts import render, redirect
from django.db import transaction
from accounts.forms import WorkspaceRegistrationForm
from accounts.models import Workspace, User
from task_workspace import workspace


# Create your views here.
def register_workspace(request):
    if request.method == 'POST':
        form = WorkspaceRegistrationForm(request.POST)
        if form.is_valid():
            # Wrap database operations in a transaction to ensure atomicity
            with transaction.atomic():
                # Step 1: Create the new isolated workspace
                new_workspace = Workspace.objects.create(
                    name=form.cleaned_data['workspace_name']
                )
                
                # Step 2: Provision the user record bound to this workspace
                User.objects.create(
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password'],
                    workspace=new_workspace,
                    role=User.Role.WORKSPACE_ADMIN, # Automatically assigned Admin role
                )
            return redirect('login')
        else:
            form = WorkspaceRegistrationForm()
            
        return render(request, 'accounts/register_workspace.html', {'form':form})
    
    