from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from .models import Spend
from django.urls import reverse

def index(request):
    return HttpResponse('this is index')

def year(request, year):
    return HttpResponse('this is year')

def month(request, year, month):
    return HttpResponse('this is month')

def stock(request):
    return HttpResponse('this is stock')

def forms(request):
    return HttpResponse('this is forms')