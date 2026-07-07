from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegistoForm
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.contrib.auth.backends import ModelBackend
from django.urls import reverse

def magic_link_login(request):

    if request.method == "POST":

        email = request.POST.get("email")

        try:
            user = User.objects.get(email=email)

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            link = request.build_absolute_uri(
                reverse("magic_login_confirm", args=[uid, token])
            )

            send_mail(
                "Login mágico",
                f"Clique no link para entrar:\n\n{link}",
                None,
                [email],
                fail_silently=False,
            )

            return render(request, "accounts/link_enviado.html")

        except User.DoesNotExist:
            return render(request, "accounts/magic_login.html", {
                "erro": "Email não encontrado"
            })

    return render(request, "accounts/magic_login.html")

def magic_login_confirm(request, uidb64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except:
        user = None

    if user and default_token_generator.check_token(user, token):

        login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        return redirect('/')

    return render(request, "accounts/login_invalido.html")

def login_view(request, autor=False):

    erro = ""

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            if user.groups.filter(name="autores").exists():
                return redirect("artigos")
            else:
                return redirect("projetos")
        else:
            erro = "Utilizador ou password inválidos"

    return render(request, "accounts/login.html", {
        "erro": erro
    })

def logout_view(request):
    logout(request)
    return redirect('login')


def registo_view(request, autor=False):
    form = RegistoForm(request.POST or None)

    if form.is_valid():
        user = form.save()

        if autor:
            grupo = Group.objects.get(name="autores")
            user.groups.add(grupo)
            return redirect("login_autores")
        else:
            return redirect("login")    

    return render(request, "accounts/registo.html", {
        "form": form,
    })

def registo_autores_view(request):
    return registo_view(request, autor=True)