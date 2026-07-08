from django.urls import path
from django.contrib.auth import views as auth_views
from accounts import views

urlpatterns = [
    # 1. Public B2B Workspace Registration 
    path('register/', views.register_workspace, name='register_workspace'),  #type:ignore
    
    # 2. Secure Login / Logout
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # 3. Secure Internal Dashboards & Staff Management
    path('dashboard/', views.workspace_dashboard, name='workspace_dashboard'),
    path('add-member/', views.add_workspace_member, name='add_workspace_member'), #type:ignore
]

