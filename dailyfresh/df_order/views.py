#coding=utf-8
from django.shortcuts import render, redirect
from df_user import user_decorator
from df_user.models import *
from df_cart.models import *
from django.db import transaction
from .models import *
from datetime import datetime
from decimal import Decimal

# 订单提交页
@user_decorator.login #登陆验证
def order(request):
    data_list = request.GET.getlist('carts_id')    # 拿到购物车id的集合，是这种格式的['1','31']
    print(data_list)
    data = [int(item) for item in data_list]

    uid = request.session['user_id']
    user = UserInfo.objects.get(id=uid)
    carts = CartInfo.objects.filter(id__in=data)   # 用in方法来拿到数据集

    carts_ids = ','.join(data_list)
    # carts_ids = str(carts_ids)
    carts_ids = data
    print(carts_ids)

    context = {'title': '提交订单', 'page_name': 1,
               'user': user, 'carts': carts,
               'carts_ids': carts_ids,
               }
    return render(request, 'df_order/place_order.html', context)


'''
1.创建订单对象
2.判断库存是否足够
3.创建详单对象
4.删除购物车，减去库存
5.操作不成功就回滚
'''

@transaction.atomic()
@user_decorator.login
def order_handle(request):
    tran_id = transaction.savepoint()

    # 当前时间
    now = datetime.now()
    # 拿到当前用户的id

    try:
        uid = request.session['user_id']
        # 构建订单对象
        myorder = OrderInfo()
        myorder.oid = '%s%d'%(now.strftime('%Y%m%d%H%M%S'), uid)
        myorder.user_id = uid
        # print(myorder.oid)
        myorder.odate = now
        myorder.ototal = Decimal(request.POST.get('total'))
        myorder.oaddress = list(UserInfo.objects.filter(id=uid).values('uaddress'))[0]
        print( myorder.oaddress, myorder.odate, myorder.ototal)
        myorder.save()
        # 构建详细单对象

        carts_id = request.POST.getlist('carts[]')
        print(carts_id)
        print('传之中的carts_id', carts_id)
        carts_id1 = [int(item) for item in carts_id]
        print('传之后的carts_id',carts_id1)
        for id1 in carts_id1:
            mydetail = DetailInfo()
            mydetail.order = myorder
            cart = CartInfo.objects.get(id=id1)
            goods = cart.goods
            if goods.gkucun >= cart.ctoun:
                goods.gkucun = cart.goods.gkucun-cart.ctoun
                goods.save()
                mydetail.goods_id = goods.id
                mydetail.price = goods.gprice
                mydetail.count = cart.ctoun
                mydetail.save()

                #删除购物车
                cart.delete()
            else:
                transaction.savepoint_rollback(tran_id)
                return redirect('/cart/')

        transaction.savepoint_commit(tran_id)
    except Exception as e:
        print('===============%s'%e)
        transaction.savepoint_rollback(tran_id)

    return redirect('/user/order/')


