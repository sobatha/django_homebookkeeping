from rest_framework import serializers
from .models import Spend, Income, Card, Account, Budget

class SpendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spend
        fields = ("spend_category", "spend_date", "spend_money", "spend_memo", "spend_card")

class IncomeSperializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ("income_category", "income_date", "income_money", "income_memo")
