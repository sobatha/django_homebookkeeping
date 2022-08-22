from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.views import generic
from .models import Spend, Income, Card
from .forms import PaymentForm, IncomeForm
from django.urls import reverse, reverse_lazy
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

def index(request):
    today = datetime.now()
    now_month = today.month
    now_year = today.year
    return render(request, 'kakeibo/index.html', {'year': now_year, 'month': now_month,})

def year(request, year):
    return HttpResponse('this is year')

def month(request, year, month):
    monthly_spendlist = Spend.objects.filter(spend_date__month=month).filter(spend_date__year=year).order_by('spend_category')
    monthly_incomelist = Income.objects.filter(income_date__month=month).filter(income_date__year=year).order_by('income_category')
    now_date = datetime(int(year), int(month), 1)
    previous_date = now_date - relativedelta(months=1)
    previous_month = previous_date.month
    previous_year = previous_date.year
    next_date = now_date + relativedelta(months=1)
    next_month = next_date.month
    next_year = next_date.year
    return render(request, 'kakeibo/monthly_spend.html', 
    {'monthly_spendlist': monthly_spendlist, 'monthly_incomelist': monthly_incomelist,'year': year, 'month': month,
      'previous_month': previous_month, 'previous_year': previous_year,
      'next_month': next_month, 'next_year': next_year})

def stock(request):
    return HttpResponse('this is stock')

def PaymentCreate(request):
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('payment_create')
    else:
        form = PaymentForm
        title = "支出登録"
        return render(request, 'kakeibo/form.html', {'form':form, 'title':title})

def IncomeCreate(request):
    if request.method == "POST":
        form = IncomeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('income_create')
    else:
        form = IncomeForm
        title = "収入登録"
        return render(request, 'kakeibo/form.html', {'form':form, 'title':title})

def income_update(request, pk):
    income = get_object_or_404(Income, pk=pk)
    if request.method == "POST":
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            month = income.income_date.month
            year = income.income_date.year
            return HttpResponseRedirect(reverse('month', kwargs={'year': year, 'month': month}))
    else:
        form = IncomeForm(instance=payment)
        title = "収入登録"
        return render(request, 'kakeibo/update.html', {'form':form, 'pk': pk, 'title':title})


def income_delete(request, pk):
    income = get_object_or_404(Income, pk=pk)
    month = income.income_date.month
    year = income.income_date.year
    income.delete()
    #return render(request, 'kakeibo/test.html', {'year': year, 'month': month})
    return HttpResponseRedirect(reverse('month', kwargs={'year': year, 'month': month}))

def payment_update(request, pk):
    payment = get_object_or_404(Spend, pk=pk)
    if request.method == "POST":
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            month = payment.spend_date.month
            year = payment.spend_date.year
            return HttpResponseRedirect(reverse('month', kwargs={'year': year, 'month': month}))
    else:
        form = PaymentForm(instance=payment)
        title = "支出入力フォーム"
        return render(request, 'kakeibo/update.html', {'form':form, 'pk': pk, 'title':title})


def payment_delete(request, pk):
    payment = get_object_or_404(Spend, pk=pk)
    month = payment.spend_date.month
    year = payment.spend_date.year
    payment.delete()
    #return render(request, 'kakeibo/test.html', {'year': year, 'month': month})
    return HttpResponseRedirect(reverse('month', kwargs={'year': year, 'month': month}))

def settlement(request, year, month):
    card_withdrawal = 0
    card_withdrawal_specialcost = 0
    monthly_spend = Spend.objects.filter(spend_date__month=month).filter(spend_date__year=year).aggregate(models.Sum('spend_money'))
    monthly_income = Income.objects.filter(income_date__month=month).filter(income_date__year=year).aggregate(model.Sum('income_money'))
    balance = monthly_income - monthly_spend
    
    for card in Card.objects.all():
        monthend = datetime(int(year), int(month), card.day_close)
        startdate = monthend - relativedelta(months=2)
        closedate = monthend - relativedelta(months=1)
        card_withdrawal += Spend.objects.filter(spend_card_id=card.id).filter(spend_date__gt=startdate).filter(spend_date__lte=closedate).aggregate(models.Sum('spend_money'))
        card_withdrawal_specialcost += Spend.objects.filter(spend_date__gt=startdate).filter(spend_date__lte=closedate).filter(spend_category='special').aggregate(models.Sum('spend_money'))
    
    livingcost = 0
    
