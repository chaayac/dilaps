from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/', views.login_user, name='login'),
    url(r'^getjobs/', views.getJobs, name='getJobs')
]
