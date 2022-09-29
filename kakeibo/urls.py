from django.urls import path, reverse_lazy
from . import views

app_name = "kakeibo"

urlpatterns = [
    path("top", views.top, name="top"),
    path("", views.index, name="index"),
    path("budget/", views.BudgetCreateView.as_view(success_url=reverse_lazy('kakeibo:index')), name="budget"),
    path("<int:year>/<int:month>/", views.month, name="month"),
    path("settlement/<int:year>/<int:month>", views.settlement, name="settlement"),
    path("assets/", views.Assetslist, name="assets"),
    path("payment_forms/", views.PaymentCreate.as_view(success_url=reverse_lazy('kakeibo:payment_create')), name="payment_create"),
    path("income_forms/", views.IncomeCreate, name="income_create"),
    path("payment_delete/<int:pk>", views.payment_delete, name="payment_delete"),
    path("payment_update/<int:pk>", views.payment_update, name="payment_update"),
    path("income_delete/<int:pk>", views.income_delete, name="income_delete"),
    path("income_update/<int:pk>", views.income_update, name="income_update"),
    path("card_list/", views.Card_list.as_view(), name="card_list"),
    path("setting_card/", views.card_create, name="card_create"),
    path("card_delete/<int:pk>", views.card_delete, name="card_delete"),
    path("card_update/<int:pk>", views.card_update, name="card_update"),
]
