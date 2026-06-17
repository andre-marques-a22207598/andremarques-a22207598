from ninja import NinjaAPI
from .models import Banda, Musico, Instrumento, Concerto
from .schemas import ErrorSchema, BandaIn, BandaOut, MusicoIn, MusicoOut, InstrumentoIn, InstrumentoOut, ConcertoIn, ConcertoOut, BandaDetail, ErrorSchema

api = NinjaAPI()

#BANDAS

@api.get("/bandas", response=list[BandaOut], tags=["Bandas"])
def listar_bandas(request):
    return Banda.objects.all()

@api.post(
    "/bandas",
    response={
        201: BandaOut,
        400: ErrorSchema
    },
    tags=["Bandas"]
)
def criar_banda(request, banda_in: BandaIn):
    if Banda.objects.filter(nome=banda_in.nome).exists():
        return 400, {"detail": "Já existe uma banda com esse nome"}

    banda = Banda.objects.create(**banda_in.dict())
    return 201, banda

@api.delete("/bandas/{banda_id}", response={204: None, 404: ErrorSchema}, tags=["Bandas"])
def deletar_banda(request, banda_id: int):
    try:
        banda = Banda.objects.get(id=banda_id)
        banda.delete()
        return 204, None
    except Banda.DoesNotExist:
        return 404, {"detail": "Banda não encontrada"}

@api.put("/bandas/{banda_id}", response=BandaOut, tags=["Bandas"])
def atualizar_banda(request, banda_id: int, banda_in: BandaIn):
    banda = Banda.objects.get(id=banda_id)

    for attr, value in banda_in.dict().items():
        setattr(banda, attr, value)

    banda.save()
    return banda


#MUSICOS


@api.get("/musicos", response=list[MusicoOut], tags=["Musicos"])
def listar_musicos(request):
    return Musico.objects.all()

@api.post("/musicos", response=MusicoOut, tags=["Musicos"])
def criar_musico(request, musico_in: MusicoIn):
    if Musico.objects.filter(nome=musico_in.nome).exists():
        return 400, {"detail": "Já existe um musico com esse nome"}

    musico = Musico.objects.create(**musico_in.dict())
    return 201, musico

@api.get("/instrumentos", response=list[InstrumentoOut], tags=["Instrumentos"])
def listar_instrumentos(request):
    return Instrumento.objects.all()

@api.get("/concertos", response=list[ConcertoOut], tags=["Concertos"])
def listar_concertos(request):
    return Concerto.objects.all()

