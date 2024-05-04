from django import forms
from .models import User
from django.contrib.auth.models import User

class UsuarioForm(forms.ModelForm):
    def save(self, commit=True):
        user = super(UsuarioForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password']) #setando a senha do usuário
        user.is_active = True
        user.is_staff = False
        user.is_superuser = False
        if commit:
            user.save()
        return user

    
    class Meta:
        model = User
        fields = ["username","full_name","email", "password"]