from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from clients.models import Client
from task_workspace import workspace

# Create your views here.
@login_required #type:ignore
def client_list(request):
    # Security: Extract the workspace directly from the user's logged-in profile, ensuring that we only fetch clients for the current tenant.
    current_workspace = request.user.workspace
    
    # Using our custom manager to isolate the client roster completely to the current workspace.
    clients = Client.objects.for_workspace(workspace=current_workspace)     #type:ignore
    
    context = {
        'clients': clients
    }
    return render(request, 'clients/client_list.html', context)