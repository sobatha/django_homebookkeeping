from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
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
    return render(request, "kakeibo/top.html")


# 予算登録
@login_required
def budgetCreate(request):
    if request.method == "POST":
        form = BudgetForm(request.POST)
        if form.is_valid():
            Budget.objects.update_or_create(
                user=request.user,
                defaults={
                    "livingcost": form.cleaned_data.get("livingcost"),
                    "specialcost": form.cleaned_data.get("specialcost"),
                },
            )
            messages.success(request, "登録ができました！")
            return redirect("kakeibo:index")
    else:
        budget = Budget.objects.filter(user=request.user).first()
        title = "予算登録"
        if budget != None:
            initial_values = {"livingcost": budget.livingcost, "specialcost": budget.specialcost}
            form = BudgetForm(initial_values)
        else:
            form = BudgetForm
        return render(request, "kakeibo/form.html", {"form": form, "title": title})


def index(request):
    today = datetime.now()
    now_month = today.month
    now_year = today.year
    return render(
        request,
        "kakeibo/index.html",
        {
            "year": now_year,
            "month": now_month,
        },
    )


@login_required
def month(request, year, month):
    income_by_user = Income.objects.filter(user=request.user)
    monthly_spendlist = Spend.objects.spend_thismonth(year, month).filter(user=request.user).order_by("spend_category")
    monthly_incomelist = Income.objects.earn_thismonth(year, month).filter(user=request.user).order_by("income_category")
    monthly_payment = sum([payment.spend_money for payment in monthly_spendlist])
    monthly_income = sum([income.income_money for income in monthly_incomelist])
    income_payment = monthly_income - monthly_payment
    now_date = datetime(int(year), int(month), 1)
    previous_date = now_date - relativedelta(months=1)
    previous_month = previous_date.month
    previous_year = previous_date.year
    next_date = now_date + relativedelta(months=1)
    next_month = next_date.month
    next_year = next_date.year

    return render(
        request,
        "kakeibo/monthly_spend.html",
        {
            "monthly_spendlist": monthly_spendlist,
            "monthly_incomelist": monthly_incomelist,
            "year": year,
            "month": month,
            "previous_month": previous_month,
            "previous_year": previous_year,
            "next_month": next_month,
            "next_year": next_year,
            "monthly_payment": monthly_payment,
            "monthly_income": monthly_income,
            "income_payment": income_payment,
        },
    )

@login_required
def Assetslist(request):
    queryset = Account.objects.filter(user=request.user).order_by('-id')[:10]
    month=[]
    money=[]
    account_name=[]
    for account in queryset:
        month.append(account.closed_in_year+account.closed_on_month)
        money.append(account.amount)
        account_name.append(account.account_name)

    return render(request, 'kakeibo/account_list.html',{
        'account_name':account_name,
        'month':month,
        'money':money,
        'object_list':queryset,
    })

# 支出の登録・更新・削除
@login_required
def PaymentCreate(request):
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            payment.save()
            messages.success(request, "支出登録ができました！")
            return redirect("kakeibo:payment_create")
    else:
        form = PaymentForm()
        form.fields["spend_card"].queryset = Card.objects.filter(user=request.user)
        title = "支出登録"
        return render(request, "kakeibo/form.html", {"form": form, "title": title})


@login_required
def payment_update(request, pk):
    payment = get_object_or_404(Spend, pk=pk)
    if request.user != payment.user:
        raise Http404

    if request.method == "POST":
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            month = payment.spend_date.month
            year = payment.spend_date.year
            messages.success(request, "支出更新ができました！")
            return HttpResponseRedirect(reverse("kakeibo:month", kwargs={"year": year, "month": month}))
        else:
            messages.error(request, "入力が不正です")
    else:
        form = PaymentForm(instance=payment)
        title = "支出入力フォーム"
        return render(request, "kakeibo/update.html", {"form": form, "pk": pk, "title": title})


@login_required
def payment_delete(request, pk):
    payment = get_object_or_404(Spend, pk=pk)
    month = payment.spend_date.month
    year = payment.spend_date.year
    payment.delete()
    messages.success(request, "削除されました！")
    return HttpResponseRedirect(reverse("kakeibo:month", kwargs={"year": year, "month": month}))


# 収入の登録・更新・削除
@login_required
def IncomeCreate(request):
    if request.method == "POST":
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            messages.success(request, "収入登録ができました！")
            return redirect("kakeibo:income_create")
        else:
            messages.error(request, "入力が不正です")
    else:
        form = IncomeForm
        title = "収入登録"
        return render(request, "kakeibo/form.html", {"form": form, "title": title})


@login_required
def income_update(request, pk):
    income = get_object_or_404(Income, pk=pk)
    if request.user != income.user:
        raise Http404

    if request.method == "POST":
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            month = income.income_date.month
            year = income.income_date.year
            messages.success(request, "登録ができました！")
            return HttpResponseRedirect(reverse("kakeibo:month", kwargs={"year": year, "month": month}))
        else:
            messages.error(request, "入力が不正です")
    else:
        form = IncomeForm(instance=income)
        title = "収入登録"
        return render(request, "kakeibo/update.html", {"form": form, "pk": pk, "title": title})


@login_required
def income_delete(request, pk):
    income = get_object_or_404(Income, pk=pk)
    month = income.income_date.month
    year = income.income_date.year
    income.delete()
    messages.success(request, "削除されました！")
    return HttpResponseRedirect(reverse("kakeibo:month", kwargs={"year": year, "month": month}))


# カードのリスト・登録・更新・削除
class Card_list(LoginRequiredMixin, generic.ListView):
    template_name = "card_list.html"

    def get_queryset(self):
        user = self.request.user
        queryset = Card.objects.filter(user=self.request.user)
        return queryset


@login_required
def card_create(request):
    if request.method == "POST":
        form = CardForm(request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.user = request.user
            card.save()
            messages.success(request, "登録されました！")
            return redirect("kakeibo:card_list")
        else:
            messages.error(request, "入力が不正です")

    else:
        form = CardForm
        title = "カード入力フォーム"
        return render(request, "kakeibo/form.html", {"form": form, "title": title})


@login_required
def card_update(request, pk):
    card = get_object_or_404(Card, pk=pk)
    if request.method == "POST":
        form = CardForm(request.POST, instance=card)
        if form.is_valid():
            form.save()
            messages.success(request, "登録されました！")
            return redirect("kakeibo:card_list")
        else:
            messages.error(request, "入力が不正です")
    else:
        form = CardForm(instance=card)
        title = "カード情報更新"
        return render(request, "kakeibo/update.html", {"form": form, "pk": pk, "title": title})


@login_required
def card_delete(request, pk):
    card = get_object_or_404(Card, pk=pk)
    card.delete()
    messages.success(request, "削除されました")
    return redirect("kakeibo:card_list")


@login_required
def settlement(request, year, month):
    spend_by_user = Spend.objects.filter(user=request.user)
    income_by_user = Income.objects.filter(user=request.user)
    budget_by_user = Budget.objects.filter(user=request.user)
    card_withdrawal = 0
    card_withdrawal_specialcost = 0
    previous_card_withdrawal = 0
    monthly_payment_sum = spend_by_user.filter(spend_date__month=month).filter(spend_date__year=year)
    monthly_spend_living = sum(
        [payment.spend_money for payment in monthly_payment_sum.exclude(spend_category="special")]
    )
    monthly_spend_special = sum(
        [payment.spend_money for payment in monthly_payment_sum.filter(spend_category="special")]
    )
    monthly_income_sum = income_by_user.filter(income_date__month=month).filter(income_date__year=year)
    monthly_income = sum([income.income_money for income in monthly_income_sum])
    now_date = datetime(int(year), int(month), 1)
    previous_date = now_date - relativedelta(months=1)
    previous_month = previous_date.month
    previous_year = previous_date.year

    # カード引き落とし額の算定
    for card in Card.objects.all():
        monthend = datetime(int(year), int(month), card.day_close)
        startdate = monthend - relativedelta(months=2)
        closedate = monthend - relativedelta(months=1)
        previous_startdate = monthend - relativedelta(months=4)
        previous_closedate = monthend - relativedelta(months=3)
        card_withdrawal_query = (
            spend_by_user.filter(spend_card_id=card.id)
            .filter(spend_date__gt=startdate)
            .filter(spend_date__lte=closedate)
        )
        card_withdrawal_specialcost_query = (
            spend_by_user.filter(spend_card_id=card.id)
            .filter(spend_date__gt=startdate)
            .filter(spend_date__lte=closedate)
            .filter(spend_category="special")
        )
        previous_card_withdrawal_query = (
            spend_by_user.filter(spend_card_id=card.id)
            .filter(spend_date__gt=previous_startdate)
            .filter(spend_date__lte=previous_closedate)
        )
        card_withdrawal += sum([payment.spend_money for payment in card_withdrawal_query])
        card_withdrawal_specialcost += sum([payment.spend_money for payment in card_withdrawal_specialcost_query])
        previous_card_withdrawal += sum([payment.spend_money for payment in previous_card_withdrawal_query])

    if request.method == "GET":
        previous_assets_by_user = (
            Account.objects.filter(user=request.user)
            .filter(closed_on_month=previous_month)
            .filter(closed_in_year=previous_year)
        )

        initial_values = {
            "livingcost": sum([budget.livingcost for budget in budget_by_user]),
            "saving": monthly_income
            - sum([budget.livingcost for budget in budget_by_user])
            - sum([budget.specialcost for budget in budget_by_user]),
            "account_special": sum([assets.amount for assets in previous_assets_by_user.filter(account_name="special")])
            - monthly_spend_special,
            "account_living": sum([assets.amount for assets in previous_assets_by_user.filter(account_name="living")])
            - monthly_spend_living
            - previous_card_withdrawal,
            "account_saving": sum([assets.amount for assets in previous_assets_by_user.filter(account_name="saving")]),
        }

        context = {
            "month": month,
            "year": year,
            "card_withdrawal": card_withdrawal,
            "card_withdrawal_specialcost": card_withdrawal_specialcost,
            "monthly_income": monthly_income,
            "account_living_after": "",
            "account_special_after": "",
            "saving_after": "",
            "available_for_special": "",
            "form": SettlementForm(initial_values),
        }

    elif request.method == "POST":
        form = SettlementForm(request.POST)
        if not form.is_valid():
            messages.error(request, "入力が不正です")
            return render(request, "kakeibo/settlement.html", {"form": form})

        livingcost = form.cleaned_data.get("livingcost")
        saving = form.cleaned_data.get("saving")
        account_special = form.cleaned_data.get("account_special")
        account_living = form.cleaned_data.get("account_living")
        account_saving = form.cleaned_data.get("account_saving")
        account_living_after = livingcost + card_withdrawal_specialcost
        available_for_saving = monthly_income - account_living_after + account_living
        available_for_special = available_for_saving - saving
        account_special_after = account_special - card_withdrawal_specialcost + available_for_special
        saving_after = saving + account_saving

        context = {
            "month": month,
            "year": year,
            "card_withdrawal": card_withdrawal,
            "card_withdrawal_specialcost": card_withdrawal_specialcost,
            "monthly_income": monthly_income,
            "livingcost": livingcost,
            "saving": saving,
            "account_special": account_special,
            "account_living_after": account_living_after,
            "account_special_after": account_special_after,
            "saving_after": saving_after,
            "available_for_special": available_for_special,
            "form": form,
        }

        Account.objects.update_or_create(
            closed_on_month=month,
            closed_in_year=year,
            account_name="saving",
            user=request.user,
            defaults={"amount": saving_after},
        )
        Account.objects.update_or_create(
            closed_on_month=month,
            closed_in_year=year,
            account_name="living",
            user=request.user,
            defaults={"amount": account_living_after},
        )
        Account.objects.update_or_create(
            closed_on_month=month,
            closed_in_year=year,
            account_name="special",
            user=request.user,
            defaults={"amount": account_special_after},
        )
        messages.success(request, "決算完了！お金を移動してね")
    return render(request, "kakeibo/settlement.html", context)
