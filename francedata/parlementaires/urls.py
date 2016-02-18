from django.conf.urls import patterns, include, url

from . import views


urlpatterns = patterns('',
    url(
        r'(?P<slug>[\w-]+)/votes/$',
        views.ParlementaireVoteListView.as_view(),
        name='parlementaire_parlementaire_vote_list',
    ),
    url(
        r'tous-les-parlementaires/$',
        views.ParlementaireListView.as_view(),
        name='parlementaire_parlementaire_list',
    ),
    url(
        r'(?P<slug>[\w-]+)/$',
        views.ParlementaireDetailView.as_view(),
        name='parlementaire_parlementaire_detail',
    ),
)
