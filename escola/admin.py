from django.contrib import admin
from .models import Aluno

class AlunoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'idade', 'curso')
    ordering = ('nome',)
    search_fields = ('nome', 'curso')
    list_filter = ('curso',)
admin.site.register(Aluno, AlunoAdmin)

