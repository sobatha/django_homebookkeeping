from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView



app_name ='accounts'

urlpatterns =[
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('registration/', CreateView.as_view(
        template_name='accounts/register.html',
        form_class=UserCreationForm,
        success_url='http://0.0.0.0:8000/kakeibo/'
    ), name='registration')
]
      
