#coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import *
from df_user.views import *
# 购物车

@user_decorator.login    # 登陆验证
def cart(request):
    uid = request.session['user_id']
    carts = CartInfo.objects.filter(user_id=uid)
    carts_len = len(carts)
    request.session['carts_count'] = carts_len
    context = {'title':'购物车', 'page_name':1, 'carts': carts, 'carts_len':carts_len}
    return render(request, 'df_cart/cart.html', context)


@user_decorator.login    # 登陆验证
def add(request ,gid, count):
    uid = request.session['user_id']
    carts = CartInfo.objects.filter(user_id=uid, goods_id=int(gid))

    if len(carts) >= 1:
        cart = carts[0]
        cart.ctoun += int(count)

    else:
        cart = CartInfo()
        cart.user_id = uid
        cart.goods_id = int(gid)
        cart.ctoun = int(count)
    cart.save()

    if request.is_ajax():
        carts_count = CartInfo.objects.filter(user_id=uid).count()
        print(carts_count)
        context = {'carts_count': carts_count}
        return JsonResponse(context)

    else:
        context = {'title': '购物车', 'page_name': 1}
        return redirect('/cart/')


# 修改时更新数据库数量
@user_decorator.login
def edit(request ,cart_id, count):
    try:
        cart = CartInfo.objects.get(id=int(cart_id))
        cart.ctoun = int(count)
        cart.save()
        context = {'ok': 0}
    except Exception as e:
        context = {'ok':1}

    finally:
        return JsonResponse(context)

# 删除购物车某条信息的时候，将数据库的某条信息也删除
@user_decorator.login
def dele(request, cart_id):
    try:
        cart = CartInfo.objects.get(id=int(cart_id))
        cart.delete()
        context = {'ok':0}
    except Exception as e:
        context = {'ok':1}
    finally:
        return JsonResponse(context)
