from django.shortcuts import render, redirect
from django.db import transaction
from accounts.forms import WorkspaceRegistrationForm, AddMemberForm
from accounts.models import Workspace, User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied



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
                User.objects.create_user(     #type:ignore
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password'],
                    workspace=new_workspace,
                    role=User.Role.WORKSPACE_ADMIN, # Automatically assigned Admin role
                )
            return redirect('login')
    else:
        form = WorkspaceRegistrationForm()
            
    return render(request, 'accounts/register_workspace.html', {'form':form})
    
    
@login_required             #type:ignore
def add_workspace_member(request):
    # Strict Authorization Boundary Check
    if request.user.role != User.Role.WORKSPACE_ADMIN:
        raise PermissionDenied("Only Workspace Administrators (HR/IT) can create new member accounts.")
    
    if request.method == 'POST':
        form = AddMemberForm(request.POST)
        if form.is_valid():
            # The multi-tenant Security Core:
            # Fore the new account into the current logged-in Admin's workspace.
            admin_workspace = request.user.workspace
            
            User.objects.create_user(                       #type:ignore
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                workspace=admin_workspace, # Inherited directly from session tracking
                role=User.Role.MEMBER  # Regular employee status
            )
            return redirect('workspace_dashboard')
        
    else:
        form = AddMemberForm()
        
    return render(request, 'accounts/add_member.html', {'form':form})
    
@login_required              #type:ignore
def workspace_dashboard(request):
    # Fetch all users belonging strictly to the logged-in user's workspace
    # If it's a global admin, request user.workspace will be None, and we can handle that case separately.
    if request.user.workspace:
        team_members = User.objects.filter(workspace=request.user.workspace)
    else:
        team_members = User.objects.all() # Global Admin can see all users across workspaces
            
    context = {
        'team_members': team_members
    }
    return render(request, 'accounts/dashboard.html', context)