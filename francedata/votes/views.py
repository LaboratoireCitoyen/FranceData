from django.views import generic

from .models import Vote



class VoteListView(generic.ListView):
    model = Vote
    paginate_by = 20
