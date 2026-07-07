from django.urls import path
from . import views

urlpatterns = [
    path('', views.artigos_view, name='artigos'),
    path('novo/', views.novo_artigo_view, name='novo_artigo'),
    path('<int:artigo_id>/edita/', views.edita_artigo_view, name='edita_artigo'),
    path('<int:artigo_id>/like/', views.like_artigo_view, name='like_artigo'),
    path('<int:artigo_id>/comentario/', views.comentario_view, name='comentario'),
]