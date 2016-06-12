from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^harvest/$', views.HarvestView.as_view(), name="harvest"),
    url(r'^enhance/$', views.EnhanceView.as_view(), name="enhance_index"),
    url(r'^normalise/$', views.NormaliseView.as_view(), name="normalise_index"),
    url(r'^harvest/delete/(?P<uuid>[^/]+)/$', views.harvest_delete, name="harvest_delete"),
    url(r'^enhance/h/(?P<uuid>[^/]+)/$', views.enhance_harvest, name="enhance_harvest"),
]
