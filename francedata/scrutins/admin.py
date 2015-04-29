from django.contrib import admin

from .models import Scrutin


class ScrutinAdmin(admin.ModelAdmin):
    pass
admin.site.register(Scrutin, ScrutinAdmin)
