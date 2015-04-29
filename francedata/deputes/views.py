from django.views import generic

from .models import Depute


class DeputeDetailView(generic.DetailView):
    queryset = Depute.objects.select_related('scrutin', 'scrutin_dossier')
