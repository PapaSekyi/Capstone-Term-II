"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from articles.views import user_login,register,custom_logout,logout_done
from . views import home
from django.contrib.auth.views import PasswordChangeDoneView,PasswordChangeView

urlpatterns = [
    path('',home,name='home'),
    path('admin/', admin.site.urls),
    path('articles/', include('articles.urls')),
    path('login/',user_login,name="login"), 
    path('logout/',custom_logout,name="logout"),
    path('logout/done',logout_done,name="logout_done"),
    path('register/',register,name='register'),

]
