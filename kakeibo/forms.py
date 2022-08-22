from django import forms
from django.views import generic
from .models import Spend, Income

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Spend
        fields = ["spend_category", "spend_date", "spend_money", "spend_memo", "spend_card"]
        widgets = {
             'spend_category': forms.Select(attrs={'style': 'display:initial'}),
        }
        templatename = 'forms.html'

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ["income_category", "income_date", "income_money", "income_memo"]
        widgets = {
             'income_category': forms.Select(attrs={'style': 'display:initial'}),
        }
        templatename = 'forms.html'
    
    
    
