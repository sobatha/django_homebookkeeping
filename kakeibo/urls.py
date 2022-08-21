from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("<int:year>/<int:month>/", views.month, name='month'),
    path("<int:year>/", views.year, name="year"),
    path("stock/", views.stock, name='stock'),
    path("forms/", views.PaymentCreate, name='payment_create'),
    path("delete/<int:pk>",views.payment_delete,name="payment_delete"),
    path("update/<int:pk>", views.payment_update, name="payment_update")
]