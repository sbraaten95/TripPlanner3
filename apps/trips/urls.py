from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^dashboard$', views.dashboard, name='dashboard'),
    url(r'^add$', views.add, name='add'),
    url(r'^submit$', views.submit, name='submit'),
    url(r'^show/(?P<id>\d)$', views.show, name='show'),
    url(r'^join/(?P<id>\d)$', views.join, name='join')
]