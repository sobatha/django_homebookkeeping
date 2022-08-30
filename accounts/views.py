from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from .forms import LoginForm, UserRegistrationForm
from django.contrib.auth import authenticate
from django.contrib import messages


class Login(LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'


class Logout(LoginRequiredMixin, LogoutView):
    template_name = 'accounts/login.html'

def registration(request):
    if request.method == "POST":
        userform = UserRegistrationForm(request.POST)
        if userform.is_valid():
            userform.save()
            user = authenticate(username=userform.cleaned_data.get('username'), password=userform.cleaned_data.get('password'))
            login(request, user)
            
            return redirect('kakeibo/index')
        else:
            return redirect('login')

    else:
        userform = UserRegistrationForm()
        return render(request, 'accounts/register.html', {'form':userform})