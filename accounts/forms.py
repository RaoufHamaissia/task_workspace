from django import forms
from accounts.models import Workspace, User

class WorkspaceRegistrationForm(forms.Form):
    workspace_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Company Name'})
        
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'admin@company.com'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Secure Password'})
    )
    
    def clean_workspace_name(self):
        name = self.cleaned_data.get('workspace_name')
        if Workspace.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("A workspace with this name already exists.")
        return name
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email
    
class AddMemberForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'placeholder': 'employee@company.com'}
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Temporary Password'}
    ))
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("This email is already associated with an existing user.")
        return email