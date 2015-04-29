from django.contrib import admin

from .models import Depute


class DeputeAdmin(admin.ModelAdmin):
    pass
admin.site.register(Depute, DeputeAdmin)
