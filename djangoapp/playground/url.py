from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns=[
    path('hello/',views.sayhello,name='sayhello'),
    path('dowork/',views.dowork,name='dowork'),
    path('RoutersView/',views.RoutersView,name='RoutersView'),
    path('SwitchesView/',views.SwitchesView,name='SwitchesView'),
    path('FirewallView/',views.FirewallView,name='FirewallView'),
    path('RouterDoWork/',views.RouterDoWork,name='RouterDoWork'),
    path('SwitchDoWork/',views.SwitchDoWork,name='SwitchDoWork'),
    path('FirewallDoWork/',views.FirewallDoWork,name='FirewallDoWork'),
    path('api/routers/', views.RouterList, name='router_list_api'),  
    path('api/devices/', views.devices_list, name='devices_list'),
    path('api/switches/', views.SwitchList, name='switch_list_api'),
    path('api/firewalls/', views.FirewallList, name='firewall_list_api'),
    
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('approve_users/', views.approve_users, name='approve_users'),
    path('routerconfiguration/', views.routerconfiguration, name='routerconfiguration'),
    path('switchconfiguration/', views.switchconfiguration, name='switchconfiguration'),
    path('sethostname/', views.sethostname, name='sethostname'),
    path('setbanner/', views.setbanner, name='setbanner'), 
    path('setInterfaceConfigration/', views.setInterfaceConfigration, name='setInterfaceConfigration'), 
    
]