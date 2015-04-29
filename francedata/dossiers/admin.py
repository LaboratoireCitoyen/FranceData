from django.contrib import admin

from .models import Dossier


class DossierAdmin(admin.ModelAdmin):
    pass
admin.site.register(Dossier, DossierAdmin)
