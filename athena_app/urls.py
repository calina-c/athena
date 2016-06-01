from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^harvest/$', views.HarvestView.as_view(), name="harvest"),
    url(r'^enhance/$', views.enhance_index, name="enhance_index"),
    url(r'^harvest/delete/(?P<uuid>[^/]+)/$', views.harvest_delete, name="harvest_delete"),
]
