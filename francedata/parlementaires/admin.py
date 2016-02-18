from django.contrib import admin

from .models import Parlementaire


class ParlementaireAdmin(admin.ModelAdmin):
    pass

admin.site.register(Parlementaire, ParlementaireAdmin)
