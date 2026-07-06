from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# Create your models here.

class Workspace(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        
        # Superadmins don't need a workspace, but tenant admins/members do
        if not extra_fields.get('is_superuser') and not extra_fields.get('workspace'):
            raise ValueError("Regular users and Workspace Admins must be assigned to a Workspace.")
        
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', User.Role.GLOBAL_ADMIN)
        extra_fields.setdefault('workspace', None)
        
        return self.create_user(email, password, **extra_fields)
    
    
class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        GLOBAL_ADMIN = 'GLOBAL_ADMIN', 'Global Admin'
        WORKSPACE_ADMIN = 'WORKSPACE_ADMIN', 'Workspace Admin'
        MEMBER = 'MEMBER', 'Regular Member'
        
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.MEMBER)
    
    # The multi_tenant aspect: each user belongs to a workspace, except for global admins
    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='users'
    )
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = CustomUserManager()
    
    def __str__(self):
        return f"{self.email} ({self.role})"