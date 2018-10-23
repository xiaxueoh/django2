#coding=utf-8
from django.http import HttpResponse, HttpResponseRedirect

# 验证登陆了没有，没有的话转向登陆页
def login(func):
    def login_fun(request, *args, **kwargs):
        if request.session.has_key('user_id'):
            return func(request, *args, **kwargs)

        else:
            red = HttpResponseRedirect('/user/login/')
            red.set_cookie('url', request.get_full_path())  #为了提高用户体验，从哪来就返回到哪个页面
            return red
    return login_fun


