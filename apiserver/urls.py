from django.conf.urls import url, include
from django.views import generic

import api

urlpatterns = [
    url(r'^api/', include(api.router.urls)),
    url(r'^$', generic.RedirectView.as_view(url='/api/')),
]
