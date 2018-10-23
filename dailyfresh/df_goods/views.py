#coding=utf-8

from django.shortcuts import render,redirect
from .models import *
from django.core.paginator import Paginator
from haystack.views import SearchView
from df_cart.models import *

# 首页
def index(request):
    # 拿到每个分类里面的最新、最热的4条数据
    typelist = TypeInfo.objects.all()
    type0 = typelist[0].goodsinfo_set.order_by('-id')[0:4]
    type01 = typelist[0].goodsinfo_set.order_by('-gclick')[0:4]

    type1 = typelist[1].goodsinfo_set.order_by('-id')[0:4]
    type11 = typelist[1].goodsinfo_set.order_by('-gclick')[0:4]

    type2 = typelist[2].goodsinfo_set.order_by('-id')[0:4]
    type21 = typelist[2].goodsinfo_set.order_by('-gclick')[0:4]

    type3 = typelist[3].goodsinfo_set.order_by('-id')[0:4]
    type31 = typelist[3].goodsinfo_set.order_by('-gclick')[0:4]

    type4 = typelist[4].goodsinfo_set.order_by('-id')[0:4]
    type41 = typelist[4].goodsinfo_set.order_by('-gclick')[0:4]

    type5 = typelist[5].goodsinfo_set.order_by('-id')[0:4]
    type51 = typelist[5].goodsinfo_set.order_by('-gclick')[0:4]

    # 从session拿到购物车数量
    if request.session.has_key('user_id'):
        carts_count = CartInfo.objects.filter(user_id=request.session['user_id']).count()
    else:
        carts_count = 0

    context = {
               'title':'首页', 'guest_cart':1,
               'type0': type0, 'type01': type01,
               'type1': type1, 'type11': type11,
               'type2': type2, 'type21': type21,
               'type3': type3, 'type31': type31,
               'type4': type4, 'type41': type41,
               'type5': type5, 'type51': type51,
               'carts_count':carts_count

               }
    return render(request, 'df_goods/index.html', context)


# 列表页
def list(request, tid, pindex, sort):
    typeinfo = TypeInfo.objects.get(id=int(tid))
    news = typeinfo.goodsinfo_set.order_by('-id')[0:2]

    # 默认排序
    if sort == '1':
        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-id')
    # 价格排序
    if sort == '2':
        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-gprice')
    # 人气排序
    if sort == '3':
        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-gclick')


    # 使用Paginator 作分页

    paginator = Paginator(goods_list, 5)

    # 获得每页的数据
    page = paginator.page(int(pindex))


    context = {
               'title':typeinfo.ttitle, 'guest_cart':1,
               'news':news, 'page':page,
               'paginator':paginator, 'typeinfo':typeinfo,
               'sort':sort
                }


    return render(request, 'df_goods/list.html', context)

# 详情页
def detail(request, id):
    goods = GoodsInfo.objects.get(id=int(id))
    news_type = TypeInfo.objects.get(id=goods.gtype_id)
    news = news_type.goodsinfo_set.order_by('-id')[0:2]
    goods.gclick +=1
    goods.save()

    try:
        carts_count = request.session['carts_count']

    except:
        carts_count = 0
    context = {
               'title':goods.gtitle, 'guest_cart':1,
               'news':news, 'g':goods, 'id':id,
                'carts_count':carts_count
              }


    response = render(request, 'df_goods/detail.html', context)

    # 最近把最近浏览的商品信息存到cookie
    goods_ids = request.COOKIES.get('goods_ids', '')    # 先取到cookie里面的数据
    goods_id = '%s'%goods.id                            # 把id转成字符串

    if goods_ids != '':                                  # 判断是否为非空
        goods_ids1 = goods_ids.split(',')                # 拆分为列表

        if goods_ids1.count(goods_id) >= 1:  # 如果该商品多次点击，会把最新一次放到列表最前面，而且把重复的删除
            goods_ids1.remove(goods_id)
        goods_ids1.insert(0, goods_id)


        if len(goods_ids1) >= 6:
            # 控制数量为5
            del goods_ids1[5]
        goods_ids = ','.join(goods_ids1)
            # 拼接成字符串


    else:
        goods_ids = goods_id
        # 如果为空，直接写入cookie


    response.set_cookie('goods_ids', goods_ids)
    return response


# 购物车数量
def carts_count(request):
    if request.session.has_key('user_id'):
        return CartInfo.objects.filter(user_id=request.session['user_id']).count()
    else:
        return 0

class MySearchView(SearchView):
    def extra_context(self):
        context = super(MySearchView, self).extra_context()
        context['title']:'搜索'
        context['guest_cart']=1
        context['carts_count']=carts_count(self.request)
        return context
