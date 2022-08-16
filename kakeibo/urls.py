from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("<int:year>/<int:month>/", views.month, name='month'),
    path("<int:year>/", views.year, name="year"),
    path("stock/", views.stock, name='stock'),
    path("forms/", views.forms, name='form'),
]