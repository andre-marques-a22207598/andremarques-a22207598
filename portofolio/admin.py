from django.contrib import admin
from .models import (
    Owner,
    Universidade,
    Licenciatura,
    Formacao,
    Docente,
    UnidadeCurricular,
    Tecnologia,
    Projeto
)

# Register your models here.
@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ('nome', 'titulo', 'email')

    def has_add_permission(self, request):
        # só permite 1 perfil
        if Owner.objects.exists():
            return False
        return True

@admin.register(Universidade)
class UniversidadeAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Licenciatura)
class LicenciaturaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'duracao', 'universidade')
    search_fields = ('nome',)
    list_filter = ('universidade',)

@admin.register(Formacao)
class FormacaoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'instituicao', 'inicio', 'fim')
    search_fields = ('titulo', 'instituicao')
    list_filter = ('inicio',)

@admin.register(Docente)
class DocenteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'pagina')
    search_fields = ('nome',)

@admin.register(UnidadeCurricular)
class UnidadeCurricularAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ano', 'semestre', 'ects', 'licenciatura')
    search_fields = ('nome',)
    list_filter = ('ano', 'semestre', 'licenciatura')

@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data', 'destaque', 'unidade_curricular')
    search_fields = ('titulo', 'descricao')
    list_filter = ('destaque', 'data', 'unidade_curricular')

    filter_horizontal = ('tecnologias',)
