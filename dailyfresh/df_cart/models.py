#coding=utf-8
from django.db import models

class CartInfo(models.Model):
    user = models.ForeignKey('df_user.UserInfo', on_delete=None)
    goods = models.ForeignKey('df_goods.GoodsInfo', on_delete=None)
    ctoun = models.IntegerField()
