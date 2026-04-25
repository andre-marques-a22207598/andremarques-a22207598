from django.shortcuts import render
from .models import Curso, Professor, Aluno

def curso_view(request, id):
    curso=Curso.objects.get(id=id)       
    return render(request, 'escola/curso.html', {'curso': curso})

def cursos_view(request):

    cursos = (
        Curso.objects
        .select_related('professor')
        .prefetch_related('alunos')
        .all()
    )
    
    return render(request, 'escola/cursos.html', {'cursos': cursos})

def professores_view(request):
    professores = (
        Professor.objects
        .prefetch_related('cursos__alunos')
    )
    
    return render(request, 'escola/professores.html', {'professores': professores})


def alunos_view(request):

    alunos = (
    Aluno.objects
    .prefetch_related('cursos__professor')
)
    
    return render(request, 'escola/alunos.html', {'alunos': alunos})
