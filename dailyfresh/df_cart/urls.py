from django.conf.urls import url
from . import views


app_name = 'df_cart'

urlpatterns = [
    url('^$', views.cart),
    url('^add(\d+)_(\d+)/$', views.add),
    url('^edit(\d+)_(\d+)/$', views.edit),
    url('^dele(\d+)/$', views.dele),
]