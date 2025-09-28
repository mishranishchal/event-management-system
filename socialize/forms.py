from django import forms
from .models import MyModel
# from .models import Contributor

# class RegistrationForm(forms.ModelForm):
class RegistrationForm(forms.Form):
 
    email_address = forms.EmailField(label='Your email address')
    phone_number = forms.IntegerField(label='Please enter your phone number')
    
class MyForm(forms.ModelForm):
  class Meta:
    model = MyModel
    fields = ["username", "password",]
    labels = {'username': "User Name", "password": "Password",}
