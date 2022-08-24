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

class SettlementForm(forms.Form):
    livingcost = forms.IntegerField(
        label='生活費',
        required=True,
        widget=forms.TextInput(attrs={'class':'form', 'autocomplete':'off', 'placeholder':'月の生活費'})
    )

    saving = forms.IntegerField(
        label='貯金',
        required=True,
        widget=forms.TextInput(attrs={'class':'form', 'autocomplete':'off', 'placeholder':'貯金する金額'})
    )
    
    account_special = forms.IntegerField(
        label='特別費口座',
        required=True,
        widget=forms.TextInput(attrs={'class':'form', 'autocomplete':'off', 'placeholder':'特別費口座残高'})
    )

    account_living = forms.IntegerField(
        label='生活費口座',
        required=True,
        widget=forms.TextInput(attrs={'class':'form', 'autocomplete':'off', 'placeholder':'生活費口座残高'})
    )
    
    account_saving = forms.IntegerField(
        label='貯金口座',
        required=True,
        widget=forms.TextInput(attrs={'class':'form', 'autocomplete':'off', 'placeholder':'貯金口座残高'})
    )
    
