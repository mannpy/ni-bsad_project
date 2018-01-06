from django.conf.urls import url
from . import views

app_name = 'alloys'

urlpatterns = [
    url(r'^$', views.IndexList.as_view(), name='index'),
    url(r'^alloy/(?P<slug>[\w\-]+)/$', views.AlloyDetail.as_view(), name='alloy-detail')
]
