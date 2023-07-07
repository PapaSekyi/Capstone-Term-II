from django import forms
from django.contrib.auth.models import User
# Utilizing the inbuilt user model for making the users.

from . models import article


class LoginForm(forms.Form):
    username=forms.CharField(max_length=125)
    password=forms.CharField(widget=forms.PasswordInput()) 

class GenreForm(forms.Form): 
    genre=forms.CharField(max_length=255) 

class USerRegistration(forms.ModelForm):
    password = forms.CharField(label="Password",widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password",widget=forms.PasswordInput)


    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        model=User
        fields=('username','first_name','email','password','password2')
    
    # def clean_password2(self):
    #     cd=self.cleaned_data
    #     if cd['password']!=cd['password2']:
    #         raise forms.ValidationError("Passwords Don't match")
    #     return cd['password']
    
    def clean(self):

        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password and password2 and password != password2:
            print(password)
            raise forms.ValidationError("Passwords don't match")
        return cleaned_data
    

class ArticleRegistrationForm(forms.ModelForm):
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'ModelName'
        verbose_name_plural = 'ModelNames'
        model=article
        fields =('title','content')
        # Slug Published and Author will be added automatically.