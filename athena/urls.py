from django.conf.urls import include, url

urlpatterns = [
    url(r'^app/', include('athena_app.urls')),
]
