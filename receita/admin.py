from django.contrib import admin
from .models import Receita

class ReceitaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tempo_preparo')
    ordering = ('nome',)
    search_fields = ('nome',)
    list_filter = ('tempo_preparo',)
admin.site.register(Receita, ReceitaAdmin)