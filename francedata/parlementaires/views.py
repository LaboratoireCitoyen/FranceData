import datetime

from django.views import generic
from django import shortcuts
from pure_pagination.mixins import PaginationMixin

from francedata.dossiers.models import Dossier
from .models import Parlementaire


class ParlementaireDetailView(generic.DetailView):
    queryset = Parlementaire.objects.all()

    def get_context_data(self, object):
        c = super(ParlementaireDetailView, self).get_context_data()

        dossiers = Dossier.objects.filter(scrutin__vote__in=self.object.vote_set.all()
                ).distinct()

        recent = datetime.datetime.now() - datetime.timedelta(days=400)
        c['votes'] = self.object.vote_set.filter(scrutin__date__gte=recent
                ).select_related('scrutin').distinct('scrutin__dossier__titre'
                ).order_by('scrutin__dossier__titre')

        return c


class ParlementaireVoteListView(PaginationMixin, generic.ListView):
    paginate_by = 20

    def get_queryset(self):
        self.parlementaire = shortcuts.get_object_or_404(Parlementaire, slug=self.kwargs['slug'])
        return self.parlementaire.vote_set.select_related('scrutin', 'scrutin__dossier')


class ParlementaireListView(PaginationMixin, generic.ListView):
    paginate_by = 20
    queryset = Parlementaire.objects.all().order_by('nom')
