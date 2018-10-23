from django.conf.urls import url
from . import views
app_name = 'df_order'


urlpatterns = [
    url(r'^$', views.order),
    url(r'^order_handle/$', views.order_handle),
]