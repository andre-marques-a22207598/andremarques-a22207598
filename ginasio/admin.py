from django.contrib import admin
from .models import Cliente

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'idade', 'plano')
    ordering = ('nome',)
    search_fields = ('nome', 'plano')
    list_filter = ('plano',)
admin.site.register(Cliente, ClienteAdmin)