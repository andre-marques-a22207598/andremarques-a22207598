from django.db import models


class Banda(models.Model):
    nome = models.CharField(max_length=100)
    genero = models.CharField(max_length=50)
    ano_formacao = models.PositiveIntegerField()

    def __str__(self):
        return self.nome


class Instrumento(models.Model):
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)
    naipe = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


class Musico(models.Model):
    nome = models.CharField(max_length=100)
    idade = models.PositiveIntegerField()

    instrumentos = models.ManyToManyField(Instrumento)

    def __str__(self):
        return self.nome


class Concerto(models.Model):
    banda = models.ForeignKey(Banda, on_delete=models.CASCADE, related_name='concertos')
    local = models.CharField(max_length=100)
    data = models.DateField()
    capacidade = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.banda.nome} - {self.local}"