from django.contrib import admin

from .models import Groupe


class GroupeAdmin(admin.ModelAdmin):
    pass
admin.site.register(Groupe, GroupeAdmin)
