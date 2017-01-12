from django.conf.urls import include, url

from activity import views

urlpatterns = [
    url(r'^links$', views.LinkView.as_view()),
    url(r'^links/$', views.LinkView.as_view()),
]
