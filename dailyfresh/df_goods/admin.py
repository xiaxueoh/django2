from django.contrib import admin
from .models import *
# Register your models here.

class GoodsInfoDisplay(admin.ModelAdmin):
    list_display = ['id', 'gtitle', 'gpic', 'gprice', 'isDelete', 'gunit', 'gclick', 'gjianjie', 'gkucun', 'gtype']



admin.site.register(TypeInfo)
admin.site.register(GoodsInfo, GoodsInfoDisplay)

