from django.db import models
from django.conf import settings
from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

class CommonManager(models.Manager):

    def spend_thismonth(self, year, month):
        return self.get_queryset().filter(spend_date__month=month).filter(spend_date__year=year)

    def earn_thismonth(self, year, month):
        return self.get_queryset().filter(income_date__month=month).filter(income_date__year=year)


class Spend(models.Model):
    Spend_Categorys = [
        ("food", "食費"),
        ("rent", "家賃"),
        ("education", "本、学習、勉強"),
        ("amuse", "娯楽費"),
        ("utility", "水道光熱通信サブスク費"),
        ("gaget", "ガジェット"),
        ("beauty", "衣服・美容室"),
        ("dailyitem", "日用品"),
        ("special", "特別費・旅行費"),
    ]

    spend_category = models.CharField(
        max_length=15,
        choices=Spend_Categorys,
        default="food",
    )
    spend_money = models.IntegerField(default=0)
    spend_card = models.ForeignKey("Card", on_delete=models.SET_NULL, blank=True, null=True)
    spend_date = models.DateField(default=datetime.date.today)
    spend_memo = models.TextField(max_length=200, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    objects = CommonManager()

    def __str__(self):
        return self.spend_category


class Income(models.Model):
    Income_Categories = [
        ("salary", "給料"),
        ("bonus", "ボーナス"),
        ("other", "その他"),
    ]
    income_category = models.CharField(
        max_length=15,
        choices=Income_Categories,
        default="salary",
    )
    income_money = models.IntegerField(default=0)
    income_date = models.DateField(default=datetime.date.today)
    income_memo = models.TextField(max_length=200, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    objects = CommonManager()

    def __str__(self):
        return self.income_category


class Card(models.Model):
    card_name = models.CharField(max_length=10)
    day_close = models.IntegerField(default=1)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.card_name


class Account(models.Model):
    Account_Categories = [
        ("living", "生活費口座"),
        ("special", "特別費口座"),
        ("saving", "貯金口座"),
    ]
    account_name = models.CharField(max_length=9, choices=Account_Categories, default="living")
    closed_on_month = models.IntegerField(default=1)
    closed_in_year = models.IntegerField(default=2022)
    amount = models.IntegerField(default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.account_name


class Budget(models.Model):
    livingcost = models.IntegerField(default=0, blank=True, null=True)
    specialcost = models.IntegerField(default=0, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
