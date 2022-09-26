from django.urls import path, re_path
from . import views
app_name = 'web'
urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^login/', views.login_request, name='login'),
    re_path(r'^register/', views.register_request, name='register'),
    re_path(r'^fruit_series/', views.fruit_series, name='fruit_series'),
    re_path(r'^meat_series/', views.meat_series, name='meat_series'),
    path('logout/', views.logout_request, name='logout'),
    re_path(r'^purchase/', views.purchase, name='purchase'),
    re_path(r'^payment/', views.payment, name='payment'),
    re_path(r'^recipt/', views.recipt, name='recipt'),
    re_path(r'^delete/', views.delete, name='delete'),
    re_path(r'^aboutus/', views.aboutus, name='aboutus'),
    re_path(r'^discount/', views.discount, name='discount'),
    re_path(r'^info/', views.info, name='info'), ]
