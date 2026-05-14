from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from .models import (
    Owner,
    Universidade,
    Licenciatura,
    Formacao,
    Docente,
    UnidadeCurricular,
    Projeto,
    Tecnologia,
    MakingOf
)


# 🔹 INÍCIO
def inicio_view(request):
    return render(request, 'portofolio/inicio.html')


# 🔹 OWNER
def owner_detail(request):
    owner = Owner.objects.first()

    return render(request, 'portofolio/owner.html', {'owner': owner})


# 🔹 SOBRE
def sobre_view(request):
    return render(request, 'portofolio/sobre.html')

# 🔹 LICENCIATURA
def licenciatura_detail(request):
    licenciatura = Licenciatura.objects.select_related(
        'universidade'
    ).first()

    return render(request, 'portofolio/licenciatura.html', {
        'licenciatura': licenciatura
    })


# 🔹 FORMAÇÃO
def formacao_list(request):
    formacoes = Formacao.objects.select_related(
        'owner'
    ).all()
    return render(request, 'portofolio/formacoes.html', {
        'formacoes': formacoes
    })


def formacao_detail(request, id):
    formacao = get_object_or_404(Formacao, id=id)

    return render(request, 'portofolio/formacao_detail.html', {
        'formacao': formacao
    })


def apaga_formacao_view(request, formacao_id):
    formacao = get_object_or_404(Formacao, id=formacao_id)

    formacao.delete()

    return redirect('formacao_list')


# 🔹 DOCENTES
def docente_list(request):
    docentes = Docente.objects.prefetch_related(
        'ucs'
    ).all()

    return render(request, 'portofolio/docentes.html', {
        'docentes': docentes
    })


def docente_detail(request, id):
    docente = get_object_or_404(
        Docente.objects.prefetch_related('ucs'),
        id=id
    )

    return render(request, 'portofolio/docente_detail.html', {
        'docente': docente
    })


# 🔹 UCs
def uc_list(request):
    ucs = UnidadeCurricular.objects.select_related(
        'licenciatura'
    ).prefetch_related(
        'docentes'
    ).all()

    return render(request, 'portofolio/ucs.html', {
        'ucs': ucs
    })


def uc_detail(request, id):
    uc = get_object_or_404(
        UnidadeCurricular.objects.select_related(
            'licenciatura'
        ).prefetch_related(
            'docentes'
        ),
        id=id
    )

    return render(request, 'portofolio/uc_detail.html', {
        'uc': uc
    })


# 🔹 PROJETOS
def projeto_list(request):
    projetos = Projeto.objects.select_related(
        'owner',
        'unidade_curricular'
    ).prefetch_related(
        'tecnologias'
    ).all()

    return render(request, 'portofolio/projetos.html', {
        'projetos': projetos
    })


def projeto_detail(request, id):
    projeto = get_object_or_404(
        Projeto.objects.select_related(
            'owner',
            'unidade_curricular'
        ).prefetch_related(
            'tecnologias'
        ),
        id=id
    )

    return render(request, 'portofolio/projeto_detail.html', {
        'projeto': projeto
    })


def novo_projeto_view(request):
    form = ProjetoForm(request.POST or None, request.FILES)
    if form.is_valid():
        form.save()
        return redirect('projetos')
    return render(request, 'portofolio/novo_projeto.html', {'form': form})


def edita_projeto_view(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)

    form = ProjetoForm(request.POST or None, request.FILES, instance=projeto)

    if form.is_valid():
        form.save()
        return redirect('projetos')

    return render(request, 'portofolio/edita_projeto.html', {'form': form, 'projeto': projeto})


def apaga_projeto_view(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    projeto.delete()
    return redirect('projetos')


# 🔹 TECNOLOGIAS

def tecnologias_view(request):
    tecnologias = Tecnologia.objects.all()
    return render(request, 'portofolio/tecnologias.html', {
    'tecnologias': tecnologias,
    #'is_gestor': gestor_portofolio(request.user)
    })

def nova_tecnologia_view(request):
    form = TecnologiaForm(request.POST or None, request.FILES)
    if form.is_valid():
        form.save()
        return redirect('tecnologias')
    return render(request, 'portofolio/nova_tecnologia.html', {'form': form})

def edita_tecnologia_view(request, tecnologia_id):
    tecnologia = get_object_or_404(Tecnologia, id=tecnologia_id)
    form = TecnologiaForm(request.POST or None, request.FILES, instance=tecnologia)

    if form.is_valid():
        form.save()
        return redirect('tecnologias')

    return render(request, 'portofolio/edita_tecnologia.html', {'form': form})


def apaga_tecnologia_view(request, tecnologia_id):
    tecnologia = get_object_or_404(Tecnologia, id=tecnologia_id)
    tecnologia.delete()
    return redirect('tecnologias')
