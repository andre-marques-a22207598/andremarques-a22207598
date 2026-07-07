from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render


# Forms
from .forms import (
    CompetenciaForm,
    FormacaoForm,
    ProjetoForm,
    RegistoForm,
    TecnologiaForm,
)

# Models
from .models import (
    Competencia,
    Docente,
    Formacao,
    Licenciatura,
    MakingOf,
    Owner,
    Projeto,
    Tecnologia,
    Universidade,
    UnidadeCurricular,
)

# ======================================================
# PERMISSÕES
# ======================================================

def gestor_portofolio(user):
    return user.is_authenticated and user.groups.filter(
        name='gestor-portofolio'
    ).exists()


# ======================================================
# PÁGINAS
# ======================================================


def inicio_view(request):
    return render(request, 'portofolio/base.html')

def owner_detail(request):
    owner = Owner.objects.first()

    return render(request, 'portofolio/owner.html', {'owner': owner})

def sobre_view(request):
    return render(request, 'portofolio/sobre.html')

def licenciatura_detail(request):
    licenciatura = Licenciatura.objects.select_related(
        'universidade'
    ).first()

    return render(request, 'portofolio/licenciatura.html', {
        'licenciatura': licenciatura
    })


# ======================================================
# DOCENTES
# ======================================================


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


# ======================================================
# UCs
# ======================================================


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


# ======================================================
# PROJETOS
# ======================================================


def projetos(request):
    projetos = Projeto.objects.select_related(
        'unidade_curricular'
    ).prefetch_related(
        'tecnologias'
    ).all()

    return render(request, 'portofolio/projetos.html', {
        'projetos': projetos,
        'is_gestor': gestor_portofolio(request.user),
    })

@login_required
def edita_projeto_view(request, projeto_id):
    if not gestor_portofolio(request.user):
        return HttpResponse("Sem permissão.", status=403)
    projeto = get_object_or_404(Projeto, id=projeto_id)

    if request.method == "POST":
        form = ProjetoForm(request.POST, request.FILES, instance=projeto)

        if form.is_valid():
            form.save()
            return redirect("projetos")
    else:
        form = ProjetoForm(instance=projeto)

    return render(
        request,
        "portofolio/edita_projeto.html",
        {
            "form": form,
            "projeto": projeto,
        },
    )

@login_required
def novo_projeto_view(request):
    if not gestor_portofolio(request.user):
        return HttpResponse("Sem permissão.", status=403)

    form = ProjetoForm(request.POST or None, request.FILES)
    if form.is_valid():
        form.save()
        return redirect('projetos')
    return render(request, 'portofolio/novo_projeto.html', {'form': form})

@login_required
def apaga_projeto_view(request, projeto_id):
    if not gestor_portofolio(request.user):
        return HttpResponse("Sem permissão.", status=403)
    projeto = get_object_or_404(Projeto, id=projeto_id)
    projeto.delete()
    return redirect('projetos')


# ======================================================
# COMPETENCIAS
# ======================================================

def competencias_view(request):
    competencias = Competencia.objects.all()
    return render(request, 'portofolio/competencias.html', {
    'competencias': competencias,
    "is_gestor": gestor_portofolio(request.user),
    })

@login_required
def nova_competencia_view(request):
    if not gestor_portofolio(request.user):
        return HttpResponse("Sem permissão.", status=403)
    form = CompetenciaForm(request.POST or None, request.FILES)
    if form.is_valid():
        form.save()
        return redirect('competencias')
    return render(request, 'portofolio/nova_competencia.html', {'form': form})

@login_required
def edita_competencia_view(request, competencia_id):
    if not gestor_portofolio(request.user):
        return HttpResponse("Sem permissão.", status=403)
    competencia = get_object_or_404(Competencia, id=competencia_id)

    if request.method == "POST":
        form = CompetenciaForm(
            request.POST,
            request.FILES,
            instance=competencia
        )

        if form.is_valid():
            form.save()
            return redirect("competencias")
    else:
        form = CompetenciaForm(instance=competencia)

    return render(
        request,
        "portofolio/edita_competencia.html",
        {
            "form": form,
            "competencia": competencia,
        },
    )

@login_required
def apaga_competencia_view(request, competencia_id):
    if not gestor_portofolio(request.user):
        return HttpResponse("Sem permissão.", status=403)
    competencia = get_object_or_404(Competencia, id=competencia_id)
    competencia.delete()
    return redirect('competencias')


# ======================================================
# TECNOLOGIAS
# ======================================================


def tecnologias_view(request):
    tecnologias = Tecnologia.objects.all()
    return render(request, 'portofolio/tecnologias.html', {
    'tecnologias': tecnologias,
    "is_gestor": gestor_portofolio(request.user),
    })

@login_required
def nova_tecnologia_view(request):
    if not gestor_portofolio(request.user):
        return HttpResponse("Sem permissão.", status=403)
    form = TecnologiaForm(request.POST or None, request.FILES)
    if form.is_valid():
        form.save()
        return redirect('tecnologias')
    return render(request, 'portofolio/nova_tecnologia.html', {'form': form})

@login_required
def edita_tecnologia_view(request, tecnologia_id):
    if not gestor_portofolio(request.user):
        return HttpResponse("Sem permissão.", status=403)
    tecnologia = get_object_or_404(Tecnologia, id=tecnologia_id)

    if request.method == "POST":
        form = TecnologiaForm(
            request.POST,
            request.FILES,
            instance=tecnologia
        )

        if form.is_valid():
            form.save()
            return redirect("tecnologias")
    else:
        form = TecnologiaForm(instance=tecnologia)

    return render(
        request,
        "portofolio/edita_tecnologia.html",
        {
            "form": form,
            "tecnologia": tecnologia,
        },
    )

@login_required
def apaga_tecnologia_view(request, tecnologia_id):
    if not gestor_portofolio(request.user):
        return HttpResponse("Sem permissão.", status=403)
    tecnologia = get_object_or_404(Tecnologia, id=tecnologia_id)
    tecnologia.delete()
    return redirect('tecnologias')


# ======================================================
# FORMAÇÕES
# ======================================================


def formacoes_view(request):
    formacoes = Formacao.objects.all()
    return render(request, 'portofolio/formacoes.html', {
    'formacoes': formacoes,
    "is_gestor": gestor_portofolio(request.user),
    })

@login_required
def nova_formacao_view(request):
    if not gestor_portofolio(request.user):
        return HttpResponse("Sem permissão.", status=403)
    form = FormacaoForm(request.POST or None, request.FILES)
    if form.is_valid():
        form.save()
        return redirect('formacoes')
    return render(request, 'portofolio/nova_formacao.html', {'form': form}) 

@login_required
def apaga_formacao_view(request, formacao_id):
    if not gestor_portofolio(request.user):
        return HttpResponse("Sem permissão.", status=403)
    formacao = get_object_or_404(Formacao, id=formacao_id)

    if request.method == "POST":
        formacao.delete()
        return redirect("formacoes")

    return render(
        request,
        "portofolio/apaga_formacao.html",
        {
            "formacao": formacao,
        },
    )

@login_required
def edita_formacao_view(request, formacao_id):
    if not gestor_portofolio(request.user):
        return HttpResponse("Sem permissão.", status=403)
    formacao = get_object_or_404(Formacao, id=formacao_id)

    if request.method == "POST":
        form = FormacaoForm(
            request.POST,
            request.FILES,
            instance=formacao
        )

        if form.is_valid():
            form.save()
            return redirect("formacoes")
    else:
        form = FormacaoForm(instance=formacao)

    return render(
        request,
        "portofolio/edita_formacao.html",
        {
            "form": form,
            "formacao": formacao,
        },
    )
