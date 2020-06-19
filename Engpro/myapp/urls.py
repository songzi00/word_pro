from django.contrib import admin
from django.urls import path,include
from . import views


app_name = 'myauth'
urlpatterns = [
    #用户
    path('',views.index,name='index'),  #首页
    path('slogin/',views.login,name='slogin'), #登录
    path('slogout/',views.logout,name='slogout'),  #登出
    path('register/',views.register,name='register'),   #注册

    #文章
    path('movieRecommd/recommd2',views.recommd2,name='recommd2'),   #推荐算法
    path('details/<id>',views.details,name='details'),  #图书详情页
    path('search/',views.search,name='search'),   #图书搜索页
    path('word/',views.word,name='word')   #生词表
]
