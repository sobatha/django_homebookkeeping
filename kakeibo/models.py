from django.db import models
from django.utils import timezone
import datetime

class Spend(models.Model):
    Spend_Categorys = [
        ('food', '食費'),
        ('rent', '家賃'),
        ('education', '本、学習、勉強'),
        ('amuse', '娯楽費'),
        ('utility', '水道光熱通信サブスク費'),
        ('gaget', 'ガジェット'),
        ('beauty', '衣服・美容室'),
        ('dailyitem', '日用品'),
        ('special', '特別費・旅行費')
    ]
    spend_category = models.CharField(
        max_length=20,
        choices=Spend_Categorys,
        default='food',
    )
    spend_money = models.IntegerField(default=0)
    spend_date = models.DateField(default=datetime.date.today) 
    spend_memo = models.TextField(max_length=200, blank=True)

    def __str__(self):
        return self.spend_category

    def publish(self):
        self.published_date = timezone.now()
        self.save()
    
