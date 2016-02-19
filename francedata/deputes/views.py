import datetime

from django.views import generic
from django import shortcuts
from pure_pagination.mixins import PaginationMixin

from francedata.dossiers.models import Dossier
from .models import Depute


class DeputeDetailView(generic.DetailView):
    queryset = Depute.objects.all()

    def get_context_data(self, **kwargs):
        c = super(DeputeDetailView, self).get_context_data()

        recent = datetime.datetime.now() - datetime.timedelta(days=400)
        c['votes'] = self.get_vote_queryset(recent)

        return c

    def get_vote_queryset(self, recent):
        qs = self.object.vote_set.filter(scrutin__date__gte=recent
                ).select_related('scrutin').distinct('scrutin__dossier__titre'
                ).order_by('scrutin__dossier__titre')
        return qs


class DeputeVoteListView(PaginationMixin, generic.ListView):
    paginate_by = 20

    def get_queryset(self):
        self.depute = shortcuts.get_object_or_404(Depute, slug=self.kwargs['slug'])
        return self.depute.vote_set.select_related('scrutin', 'scrutin__dossier')

    def get_context_data(self):
        c = super(DeputeVoteListView, self).get_context_data()
        c['depute'] = self.depute
        return c


class DeputeListView(PaginationMixin, generic.ListView):
    paginate_by = 20

    def get_queryset(self):
        return Depute.objects.all().order_by('nom')
