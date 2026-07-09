from django.db import models
from accounts.models import Workspace


# Create your models here.
class ClientManager(models.Manager):
    """Custom manager to enforce multi-tenant data boundaries."""
    def for_workspace(self, workspace):
        # Dynamically limits database queries to the active tenant session.
        return self.get_queryset().filter(workspace=workspace)
    
class Client(models.Model):
    # The Security Anchor: Links this permanently to ONE workspace, ensuring data isolation.
    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name='clients',
    )
    
    # Core Client Profile
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Overriding the default manager with our secured tool
    objects = ClientManager()
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"