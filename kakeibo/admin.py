from django.contrib import admin
from .models import Spend, Income, Card, Account, Budget

admin.site.register(Spend)
admin.site.register(Income)
admin.site.register(Card)
admin.site.register(Account)
admin.site.register(Budget)

