from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from .models import Spend
from django.urls import reverse
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

def index(request):
    return HttpResponse('this is index')

def year(request, year):
    return HttpResponse('this is year')

def month(request, year, month):
    monthly_spendlist = Spend.objects.filter(spend_date__month=month).filter(spend_date__year=year).order_by('spend_category')
    now_date = datetime(int(year), int(month), 1)
    previous_date = now_date - relativedelta(months=1)
    previous_month = previous_date.month
    previous_year = previous_date.year
    next_date = now_date + relativedelta(months=1)
    next_month = next_date.month
    next_year = next_date.year
    return render(request, 'kakeibo/monthly_spend.html', 
    {'monthly_spendlist': monthly_spendlist, 'year': year, 'month': month,
      'previous_month': previous_month, 'previous_year': previous_year,
      'next_month': next_month, 'next_year': next_year})

    return HttpResponse('this is month')

def stock(request):
    return HttpResponse('this is stock')

def forms(request):
    return render(request, 'kakeibo/form.html', {})