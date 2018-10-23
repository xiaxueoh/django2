#coding=utf-8
from django.db import models

class OrderInfo(models.Model):
    oid = models.CharField(max_length=20, primary_key=True)
    user = models.ForeignKey('df_user.Userinfo', on_delete=None)
    odate = models.DateTimeField(auto_now=True)
    oIsPay = models.BooleanField(default=False)
    ototal = models.DecimalField(max_digits=8, decimal_places=2)
    oaddress = models.CharField(max_length=150)


class DetailInfo(models.Model):
    goods = models.ForeignKey('df_goods.GoodsInfo', on_delete=None)
    order = models.ForeignKey(OrderInfo, on_delete=None)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    count = models.IntegerField()
