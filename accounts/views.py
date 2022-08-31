from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from .forms import LoginForm, UserRegistrationForm
from django.contrib.auth import authenticate
from django.contrib import messages


class Login(SuccessMessageMixin, LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    messages = "%(username)さんようこそ！"


class Logout(LoginRequiredMixin, LogoutView):
    template_name = 'accounts/login.html'
