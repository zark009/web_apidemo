"""NewApi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from appapi import views

urlpatterns = [
    url(r'^$', views.show_api_list, name="api_list"),
    url(r'^api_list/$', views.show_api_list, name="api_list"),
    url(r'^api_list/user/$', views.show_api_user, name="show_api_user"),
    url(r'^api_list/driver/$', views.show_api_driver, name="show_api_driver"),
    url(r'^api_case/$', views.show_api_case, name="api_case"),
    url(r'^run_api/$', views.run_api, name="runapi"),
    url(r'^add_api/$', views.add_api, name="addapi"),
    url(r"^edit_api/$", views.edit_api, name="editapi"),
    url(r"^run_api_case/$", views.run_api_case, name="runapicase"),
    url(r"^add_api_case/$", views.add_api_case, name="addapicase"),
    url(r"^edit_api_case/$", views.edit_api_case, name="editapicase"),
    url(r'^get_page_data/(\d+)/$', views.get_page_data, name='get_page_data'),
    url(r'^get_app_data/$', views.get_app_data, name='get_app_data'),
    url(r'^app_list/$', views.app_list, name='app_list'),
    url(r'^add_app/$', views.add_app, name='addapp'),
    url(r'^edit_app/$', views.edit_app, name='editapp'),
    url(r'^page_list/$', views.page_list, name='page_list'),
    url(r'^add_page/$', views.add_page, name='addpage'),
    url(r'^edit_page/$', views.edit_page, name='editpage'),
    url(r'^task_list/$', views.task_list, name='task_list'),
    url(r'^add_task/$', views.add_task, name='addtask'),
    url(r'^run_task/$', views.run_task, name='runtask'),
    url(r'^taskreport/(\d+).html/$', views.taskreport),
    # url(r'^add/$', views.test_add, name='add'),
    #  url(r'^applist.html/$', views.test, name='test'),
    # url(r'^$', views.hello, name="hello"),

]
