from django.contrib import admin
from .models import Banda, Musico, Instrumento, Concerto


@admin.register(Banda)
class BandaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'genero', 'ano_formacao')


@admin.register(Musico)
class MusicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'idade', 'get_instrumentos')

    def get_instrumentos(self, obj):
        return ", ".join([i.nome for i in obj.instrumentos.all()])

    get_instrumentos.short_description = "Instrumentos"
    
@admin.register(Instrumento)
class InstrumentoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo')


@admin.register(Concerto)
class ConcertoAdmin(admin.ModelAdmin):
    list_display = ('banda', 'local', 'data', 'capacidade')