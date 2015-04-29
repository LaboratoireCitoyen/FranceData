from django.conf.urls import patterns, include, url

from . import views


urlpatterns = patterns('',
    url(
        r'(?P<slug>[\w-]+)/$',
        views.DeputeDetailView.as_view(),
        name='depute_depute_detail',
    ),
)
