from django.db import models


class Owner(models.Model):
    nome = models.CharField(max_length=100)
    titulo = models.CharField(max_length=100)
    bio = models.TextField()
    foto = models.ImageField(upload_to='perfil/')
    email = models.EmailField()
    github = models.URLField()
    linkedin = models.URLField()
    cv = models.FileField(upload_to='cv/')


class Universidade(models.Model):
    nome = models.CharField(max_length=100)


class Licenciatura(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    duracao = models.IntegerField()
    universidade = models.ForeignKey(Universidade, on_delete=models.CASCADE)


class Formacao(models.Model):
    titulo = models.CharField(max_length=100)
    instituicao = models.CharField(max_length=100)
    inicio = models.DateField()
    fim = models.DateField()
    descricao = models.TextField()
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)


class Docente(models.Model):
    nome = models.CharField(max_length=100)
    pagina = models.URLField()


class UnidadeCurricular(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    ano = models.IntegerField()
    semestre = models.IntegerField()
    ects = models.IntegerField()
    imagem = models.ImageField(upload_to='ucs/')
    licenciatura = models.ForeignKey(Licenciatura, on_delete=models.CASCADE)

    docentes = models.ManyToManyField(Docente,related_name='ucs')


class Tecnologia(models.Model):
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)
    descricao = models.TextField()
    logo = models.ImageField(upload_to='tech/')
    website = models.URLField()
    nivel = models.IntegerField()


class Projeto(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    conceitos = models.TextField()
    imagem = models.ImageField(upload_to='projetos/')
    video = models.URLField(blank=True)
    github = models.URLField()
    destaque = models.BooleanField(default=False)
    data = models.DateField()
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    unidade_curricular = models.ForeignKey(UnidadeCurricular, on_delete=models.CASCADE)

    tecnologias = models.ManyToManyField(Tecnologia)

class Tfc(models.Model):
    titulo = models.CharField(max_length=300, blank=True, null=True)

    autores = models.CharField(max_length=200, blank=True, null=True)
    orientadores = models.CharField(max_length=200, blank=True, null=True)
    licenciaturas = models.CharField(max_length=200, blank=True, null=True)

    ano = models.IntegerField(blank=True, null=True)

    sumario = models.TextField(blank=True, null=True)

    link_pdf = models.URLField(blank=True, null=True)
    imagem = models.URLField(blank=True, null=True)

    palavras_chave = models.TextField(blank=True, null=True)
    areas = models.TextField(blank=True, null=True)
    tecnologias_usadas = models.TextField(blank=True, null=True)

    rating = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.titulo or "TFC sem título"


class MakingOf(models.Model):
    titulo = models.CharField(max_length=200, blank=True, null=True)

    descricao_processo = models.TextField(blank=True, null=True)

    decisoes = models.TextField(blank=True, null=True)

    erros = models.TextField(blank=True, null=True)

    correcoes = models.TextField(blank=True, null=True)

    justificacao_modelacao = models.TextField(blank=True, null=True)

    uso_ia = models.TextField(blank=True, null=True)

    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo or "Making Of"
