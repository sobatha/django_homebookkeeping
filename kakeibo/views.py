from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Spend, Income, Card, Account, Budget
from .forms import PaymentForm, IncomeForm, SettlementForm, CardForm, BudgetForm
from django.urls import reverse, reverse_lazy
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

def top(request):
    return render(request, 'kakeibo/top.html')


#予算登録
@login_required
def budgetCreate(request):
    if request.method == "POST":
        form = BudgetForm(request.POST)
        if form.is_valid():
            Budget.objects.update_or_create(
                user=request.user,
                defaults={ "livingcost": form.cleaned_data.get('livingcost'), 
                "specialcost": form.cleaned_data.get('specialcost')})
            messages.success(request, '登録ができました！')
            return redirect('kakeibo:index')
    else:
        budget = Budget.objects.filter(user=request.user).first()
        title = "予算登録"
        if budget != None:
            initial_values = {"livingcost":budget.livingcost, "specialcost":budget.specialcost}
            form = BudgetForm(initial_values)
        else:
            form = BudgetForm
        return render(request, 'kakeibo/form.html', {'form':form, 'title':title})

def index(request):
    today = datetime.now()
    now_month = today.month
    now_year = today.year
    return render(request, 'kakeibo/index.html', {'year': now_year, 'month': now_month,})

@login_required
def month(request, year, month):
    spend_by_user = Spend.objects.filter(user=request.user)
    income_by_user = Income.objects.filter(user=request.user)
    monthly_spendlist = spend_by_user.filter(spend_date__month=month).filter(spend_date__year=year).order_by('spend_category')
    monthly_incomelist = income_by_user.filter(income_date__month=month).filter(income_date__year=year).order_by('income_category')
    monthly_payment_sum = Spend.objects.filter(spend_date__month=month).filter(spend_date__year=year)
    monthly_payment = sum([payment.spend_money for payment in monthly_payment_sum])
    monthly_income_sum = income_by_user.filter(income_date__month=month).filter(income_date__year=year)
    monthly_income = sum([income.income_money for income in monthly_income_sum])
    income_payment = monthly_income - monthly_payment
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
      'next_month': next_month, 'next_year': next_year, 'monthly_payment': monthly_payment, 'monthly_income': monthly_income,
      'income_payment': income_payment})

class Assets_list(LoginRequiredMixin, generic.ListView):
    template_name= 'account_list.html'

    def get_queryset(self):
        user = self.request.user
        queryset = Account.objects.filter(user=self.request.user)
        return queryset    
    

#支出の登録・更新・削除
@login_required
def PaymentCreate(request):
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '支出登録ができました！')
            return redirect('kakeibo:payment_create')
    else:
        form = PaymentForm
        title = "支出登録"
        return render(request, 'kakeibo/form.html', {'form':form, 'title':title})

@login_required
def payment_update(request, pk):
    payment = get_object_or_404(Spend, pk=pk)
    if request.method == "POST":
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            month = payment.spend_date.month
            year = payment.spend_date.year
            messages.success(request, '支出更新ができました！')
            return HttpResponseRedirect(reverse('month', kwargs={'year': year, 'month': month}))
        else:
            messages.error(request, '入力が不正です')
    else:
        form = PaymentForm(instance=payment)
        title = "支出入力フォーム"
        return render(request, 'kakeibo/update.html', {'form':form, 'pk': pk, 'title':title})

@login_required
def payment_delete(request, pk):
    payment = get_object_or_404(Spend, pk=pk)
    month = payment.spend_date.month
    year = payment.spend_date.year
    payment.delete()
    messages.success(request, '削除されました！')
    return HttpResponseRedirect(reverse('kakeibo:month', kwargs={'year': year, 'month': month}))

#収入の登録・更新・削除
@login_required
def IncomeCreate(request):
    if request.method == "POST":
        form = IncomeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '収入登録ができました！')
            return redirect('kakeibo:income_create')
        else:
            messages.error(request, '入力が不正です')
    else:
        form = IncomeForm
        title = "収入登録"
        return render(request, 'kakeibo/form.html', {'form':form, 'title':title})

@login_required
def income_update(request, pk):
    income = get_object_or_404(Income, pk=pk)
    if request.method == "POST":
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            month = income.income_date.month
            year = income.income_date.year
            messages.success(request, '登録ができました！')
            return HttpResponseRedirect(reverse('kakeibo:month', kwargs={'year': year, 'month': month}))
        else:
            messages.error(request, '入力が不正です')
    else:
        form = IncomeForm(instance=income)
        title = "収入登録"
        return render(request, 'kakeibo/update.html', {'form':form, 'pk': pk, 'title':title})

@login_required
def income_delete(request, pk):
    income = get_object_or_404(Income, pk=pk)
    month = income.income_date.month
    year = income.income_date.year
    income.delete()
    messages.success(request, '削除されました！')
    return HttpResponseRedirect(reverse('kakeibo:month', kwargs={'year': year, 'month': month}))

#カードのリスト・登録・更新・削除
class Card_list(LoginRequiredMixin, generic.ListView):
    template_name= 'card_list.html'
    model = Card

@login_required
def card_create(request):
    if request.method == "POST":
        form = CardForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '登録されました！')
            return redirect('kakeibo:card_list')
        else:
            messages.error(request, '入力が不正です')

    else:
        form = CardForm
        title = "カード入力フォーム"
        return render(request, 'kakeibo/form.html', {'form':form, 'title':title})

@login_required
def card_update(request, pk):
    card = get_object_or_404(Card, pk=pk)
    if request.method == "POST":
        form = CardForm(request.POST, instance=card)
        if form.is_valid():
            form.save()
            messages.success(request, '登録されました！')
            return redirect('kakeibo:card_list')
        else:
            messages.error(request, '入力が不正です')
    else:
        form = CardForm(instance=card)
        title = "カード情報更新"
        return render(request, 'kakeibo/update.html', {'form':form, 'pk': pk, 'title':title})

@login_required
def card_delete(request, pk):
    card = get_object_or_404(Card, pk=pk)
    card.delete()
    messages.success(request, '削除されました')
    return redirect('kakeibo:card_list')

@login_required
def settlement(request, year, month):
    card_withdrawal = 0
    card_withdrawal_specialcost = 0
    monthly_payment_sum = Spend.objects.filter(spend_date__month=month).filter(spend_date__year=year)
    monthly_spend = sum([payment.spend_money for payment in monthly_payment_sum])
    monthly_income_sum = Income.objects.filter(income_date__month=month).filter(income_date__year=year)
    monthly_income = sum([income.income_money for income in monthly_income_sum])
    balance = monthly_income - monthly_spend

    #カード引き落とし額の算定
    for card in Card.objects.all():
        monthend = datetime(int(year), int(month), card.day_close)
        startdate = monthend - relativedelta(months=2)
        closedate = monthend - relativedelta(months=1)
        card_withdrawal_query = Spend.objects.filter(spend_card_id=card.id).filter(spend_date__gt=startdate).filter(spend_date__lte=closedate)
        card_withdrawal_specialcost_query = Spend.objects.filter(spend_card_id=card.id).filter(spend_date__gt=startdate).filter(spend_date__lte=closedate).filter(spend_category='special')
        card_withdrawal += sum([payment.spend_money for payment in card_withdrawal_query])
        card_withdrawal_specialcost += sum([payment.spend_money for payment in card_withdrawal_specialcost_query])
    
    if request.method == "GET":
        form = SettlementForm()
        return render(request, 'kakeibo/settlement.html', {'form': form, 'month' : month, 'year' : year,})

    elif request.method == "POST":    
        form = SettlementForm(request.POST)
        if not form.is_valid():
            messages.error(request, '入力が不正です')
            return render(request, 'kakeibo/settlement.html',{'form': form})

        livingcost=form.cleaned_data.get('livingcost')
        saving=form.cleaned_data.get('saving')
        account_special=form.cleaned_data.get('account_special')
        account_living=form.cleaned_data.get('account_living')
        account_saving=form.cleaned_data.get('account_saving')
        account_living_after=livingcost+card_withdrawal_specialcost
        available_for_saving=monthly_income-account_living_after
        available_for_special = available_for_saving - saving
        account_special_after= account_special - card_withdrawal_specialcost + available_for_special 
        saving_after = saving+account_saving 

        context = {
        'month' : month,
        'year' : year,
        'card_withdrawal': card_withdrawal,
        'card_withdrawal_specialcost' : card_withdrawal_specialcost,
        'monthly_income': monthly_income,
        'livingcost': livingcost,
        'saving': saving,
        'account_special': account_special,
        'account_living_after': account_living_after,
        'account_special_after': account_special_after,
        'saving_after': saving_after,
        'available_for_special': available_for_special,
        'form': form,
        }
        
        Account.objects.update_or_create(
            closed_on_month=month, closed_in_year=year, account_name='saving',
            defaults={ "amount": saving_after }
            )
        Account.objects.update_or_create(
            closed_on_month=month, closed_in_year=year, account_name='living',
            defaults={ "amount": account_living_after }
            )
        Account.objects.update_or_create(
            closed_on_month=month, closed_in_year=year, account_name='special', 
            defaults={"amount": account_special_after }
            )
        messages.success(request, '決算完了！お金を移動してね')
        return render(request, 'kakeibo/settlement.html', context)
    else:
        return HttpResponse('不正なメソッドです', status=500)

