from django import forms
from django.views import generic
from .models import Spend

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Spend
        fields = ["spend_category", "spend_date", "spend_money", "spend_memo"]
        widgets = {
             'spend_category': forms.Select(attrs={'style': 'display:initial'}),
        }
        templatename = 'forms.html'

    
    
    
