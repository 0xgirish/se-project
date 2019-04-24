from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    password = forms.PasswordInput(required=True)
    phone = forms.IntegerField(required=True)
    
    class Meta:
        model = User
        fields = {
            'username',
            'first_name',
            'last_name',
            'phone',
            'email',
            'password',
        }

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']
        user.password = self.cleaned_data['password']

        if commit:
            user.save()
        return user

