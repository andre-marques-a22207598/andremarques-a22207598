from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path('logout/', views.logout_view, name='logout'),
    path('registo/', views.registo_view, name='registo'),
    path("registo-autores/", views.registo_autores_view, name="registo_autores"),
    path("magic-login/", views.magic_link_login, name="magic_login"),
    path("magic-login-confirm/<uidb64>/<token>/", views.magic_login_confirm, name="magic_login_confirm"),

]