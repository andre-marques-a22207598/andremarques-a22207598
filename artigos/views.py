from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test

from .forms import ArtigoForm, ComentarioForm
from .models import Artigo


def eh_autor(user):
    return (
        user.is_authenticated
        and user.groups.filter(name="autores").exists()
    )

def artigos_view(request):
    artigos = Artigo.objects.all().order_by("-data_criacao")
    comentario_form = ComentarioForm()

    return render(
        request,
        "artigos/artigos.html",
        {
            "artigos": artigos,
            "comentario_form": comentario_form,
            "is_autor": eh_autor(request.user),
        },
    )

@login_required
@user_passes_test(eh_autor)
def novo_artigo_view(request):
    form = ArtigoForm(request.POST or None, request.FILES)

    if form.is_valid():
        artigo = form.save(commit=False)
        artigo.autor = request.user
        artigo.save()
        return redirect("artigos")

    return render(
        request,
        "artigos/novo_artigo.html",
        {
            "form": form,
        },
    )


@login_required
@user_passes_test(eh_autor)
def edita_artigo_view(request, artigo_id):
    artigo = get_object_or_404(Artigo, id=artigo_id)

    if artigo.autor != request.user:
        return redirect("artigos")

    if request.method == "POST":
        form = ArtigoForm(
            request.POST,
            request.FILES,
            instance=artigo
        )

        if form.is_valid():
            form.save()
            return redirect("artigos")
    else:
        form = ArtigoForm(instance=artigo)

    return render(
        request,
        "artigos/edita_artigo.html",
        {
            "form": form,
        },
    )


@login_required
def like_artigo_view(request, artigo_id):
    artigo = get_object_or_404(Artigo, id=artigo_id)

    if request.user in artigo.likes.all():
        artigo.likes.remove(request.user)
    else:
        artigo.likes.add(request.user)

    return redirect("artigos")


@login_required
def comentario_view(request, artigo_id):
    artigo = get_object_or_404(Artigo, id=artigo_id)
    form = ComentarioForm(request.POST)

    if form.is_valid():
        comentario = form.save(commit=False)
        comentario.autor = request.user
        comentario.artigo = artigo
        comentario.save()

    return redirect("artigos")