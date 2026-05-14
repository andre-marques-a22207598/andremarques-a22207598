from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio_view, name='inicio'),   #  rota que abre diretamente a página dos cursos
    
    #Owner
    path('owner/', views.owner_detail, name='owner_detail'),
    path('sobre/', views.sobre_view, name='sobre'),

    #Formação
    path('formacao/', views.formacao_list, name='formacao_list'),
    path('formacao/<int:id>/', views.formacao_detail, name='formacao_detail'),
    path('formacao/<int:formacao_id>/apaga/', views.apaga_formacao_view, name='apaga_formacao'),

    #Docentes
    path('docentes/', views.docente_list, name='docente_list'),
    path('docentes/<int:id>/', views.docente_detail, name='docente_detail'),

    #Unidades Curriculares
    path('ucs/', views.uc_list, name='uc_list'),
    path('ucs/<int:id>/', views.uc_detail, name='uc_detail'),

    #Projetos
    path('projetos/', views.projeto_list, name='projeto_list'),
    path('projetos/<int:id>/', views.projeto_detail, name='projeto_detail'),
    path('projeto/novo/', views.novo_projeto_view, name='novo_projeto'),
    path('projeto/<int:projeto_id>/edita/', views.edita_projeto_view, name='edita_projeto'),
    path('projeto/<int:projeto_id>/apaga/', views.apaga_projeto_view, name='apaga_projeto'),

    #Tecnologias
    path('tecnologias/', views.tecnologias_view, name='tecnologias'),
    path('tecnologia/novo/', views.nova_tecnologia_view, name='nova_tecnologia'),
    path('tecnologia/<int:tecnologia_id>/edita/', views.edita_tecnologia_view, name='edita_tecnologia'),
    path('tecnologia/<int:tecnologia_id>/apaga/', views.apaga_tecnologia_view, name='apaga_tecnologia'),
]