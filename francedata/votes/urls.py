from django.conf.urls import patterns, include, url

from . import views


urlpatterns = patterns('',
    url(
        r'$',
        views.VoteListView.as_view(),
        name='votes_vote_list',
    ),
)
