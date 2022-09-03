from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView, TemplateView



app_name ='accounts'

urlpatterns =[
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('logout/success/', TemplateView.as_view(
        template_name='accounts/logout.html',
        ), name='registration'),
    path('registration/', CreateView.as_view(
        template_name='accounts/register.html',
        form_class=UserCreationForm,
        success_url='https://mykakeibo.herokuapp.com/kakeibo/'
    ), name='registration')
]
      
