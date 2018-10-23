#coding=utf-8
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from df_user.models import *
from hashlib import sha1
from . import user_decorator
from df_goods.models import *
from df_order.models import *

def register(request):
    context = {'title':'天天新鲜-注册'}
    return render(request, 'df_user/register.html',context)

def register_handle(request):

    # 接收用户输入的数据
    post = request.POST
    uname = post.get('user_name')
    upwd =post.get('pwd')
    upwd2 = post.get('cpwd')
    uemail = post.get('email')

    # 判断两次的密码
    # 两次不一样：重定向到注册页面
    if upwd != upwd2:
        return redirect('/user/register/')

    #两次一样：
    else:
        # 将密码加密
        s1 = sha1()
        s1.update(upwd.encode('utf-8'))
        upwd3 = s1.hexdigest()

        #把用户输入存到数据库
        user = UserInfo()
        user.uname = uname
        user.upwd = upwd3
        user.uemail = uemail
        user.save()
        # 跳转到登陆页面
        return redirect('/user/login/')

# 判断用户名是否已经存在
def register_exist(request):
    get_name = request.GET.get('uname')
    count = UserInfo.objects.filter(uname=get_name).count()
    context = {'count':count}
    return JsonResponse(context)

# 登陆页面
def login(request):
    # 读取cookie的用户名,如果uname不存在，就返回默认值-->空
    uname = request.COOKIES.get('uname', '')
    context = {'title': '天天新鲜-登陆', 'error_name': 0, 'error_pwd': 0, 'uname': uname}
    return render(request, 'df_user/login.html',context)

# 处理登陆页面用户提交的数据
def login_handle(request):

    # 拿到用户输入的数据
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    uremember = post.get('remember', 0) # remember的值默认是等于0，就是不选中就是0

    #密码加密处理
    s1 = sha1()
    s1.update(upwd.encode('utf-8'))
    upwd2 = s1.hexdigest()

    #根据用户名查询数据库
    get_data = UserInfo.objects.filter(uname=uname)

    #判断该用户名是否存在，如果不存在，get_data是一个一个空列表
    if len(get_data) == 1:
        # 接着判断密码是否正确
        # 密码正确就跳转到用户中心页面
        if get_data[0].upwd == upwd2:
           url = request.COOKIES.get('url', '/')
           red = redirect(url)

           # 判断用户是否有选择记住密码，如果有，就存cookie
           if uremember !=0:
               red.set_cookie('uname', uname)

           # 否则存空
           else:
               red.set_cookie('uname', '', max_age=-1)

           # 存session
           request.session['user_id'] = get_data[0].id
           request.session['user_name'] = uname

           return red

        # 密码不正确就带着密码错误信息返回
        else:
            context = {'title':'天天新鲜-登陆', 'error_name':0, 'error_pwd':1, 'uname':uname, 'upwd':upwd}
            return render(request, 'df_user/login.html', context)

    # len(get_data) == 0的时候，带着用户名错误的信息返回
    else:
        context = {'title': '天天新鲜-登陆', 'error_name': 1, 'error_pwd': 0, 'uname': uname, 'upwd': upwd}
        return render(request, 'df_user/login.html', context)


@user_decorator.login
def info(request):
    uemail = UserInfo.objects.get(id=request.session['user_id']).uemail
    uname = request.session['user_name']


    # 最近浏览的内容，从cookie中读取
    goods_ids = request.COOKIES.get('goods_ids', '')
    goods_ids1 = goods_ids.split(',')
    goods_near = []
    if goods_ids1[0] != '':
        print(goods_ids1)
        for id in goods_ids1:
            goods_near.append(GoodsInfo.objects.get(id=int(id)))

    context = {'title': '用户中心',
               'uname': uname,
               'uemail': uemail,
               'page_name': 1,
               'goods_near': goods_near}
    return render(request, 'df_user/user_center_info.html', context)


@user_decorator.login
def order(request):
    orders = OrderInfo.objects.all()
    # for order in orders:
    #     for detail in order.detailinfo_set.all():
    #         print(detail)
    #print(order)
    context = {'title': '用户中心', 'page_name':1, 'orders': orders}
    return render(request, 'df_user/user_center_order.html', context)

@user_decorator.login
def site(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        post = request.POST
        uname = post.get('uname')
        uaddress = post.get('uaddress')
        uyoubian = post.get('uyoubian')
        uphone = post.get('uphone')

        #存到数据库
        user.uname = uname
        user.uaddress = uaddress
        user.uyoubian = uyoubian
        user.uphone = uphone
        user.save()

    # context = {'title': '用户中心', 'uname':uname, 'uaddress':uaddress, 'uyoubian':uyoubian, 'uphone':uphone}

    context = {'title': '用户中心', 'user':user, 'page_name':1}

    return render(request, 'df_user/user_center_site.html', context)


# 退出登陆

def logout(request):
    request.session.flush()
    return redirect('/')


# 支付
def pay(request, oid):
    return JsonResponse()

