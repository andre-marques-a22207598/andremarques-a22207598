from django.contrib import admin
from .models import Festival

class FestivalAdmin(admin.ModelAdmin):
    list_display = ('nome', 'local', 'data')
    ordering = ('data',)
    search_fields = ('nome', 'local')
    list_filter = ('data',)
admin.site.register(Festival, FestivalAdmin)