from django.db import models
from django.forms.widgets import TextInput
from django.contrib.auth.models import User
# Create your models here.

class article(models.Model):
    title = models.CharField(max_length=250)    
    slug=models.SlugField(max_length=100,unique=True) 
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    published=models.DateTimeField(auto_now_add=True)
    content= models.TextField()
