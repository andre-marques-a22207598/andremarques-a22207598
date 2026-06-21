from ninja import NinjaAPI
from .models import Banda, Musico, Instrumento, Concerto
from .schemas import ErrorSchema, BandaIn, BandaOut, MusicoIn, MusicoOut, InstrumentoIn, InstrumentoOut, ConcertoIn, ConcertoOut, BandaDetail, ErrorSchema

api = NinjaAPI()

#CONCERTOS

@api.get("/concertos", response=list[ConcertoOut], tags=["Concertos"])
def listar_concertos(request):

    # select_related porque banda é ForeignKey
    return Concerto.objects.select_related("banda")

@api.get("/concertos/{concerto_id}", response=ConcertoOut, tags=["Concertos"])
def detalhar_concerto(request, concerto_id: int):
    try:
        # select_related porque banda é ForeignKey
        concerto = Concerto.objects.select_related("banda").get(id=concerto_id)
        return concerto
    except Concerto.DoesNotExist:
        return 404, {"detail": "Concerto não encontrado"}

@api.post("/concertos", response=ConcertoOut, tags=["Concertos"])
def criar_concerto(request, concerto_in: ConcertoIn):
    try:
        banda = Banda.objects.get(id=concerto_in.banda_id)
    except Banda.DoesNotExist:
        return 404, {"detail": "Banda não encontrada"}

    concerto = Concerto.objects.create(
        banda=banda,
        local=concerto_in.local,
        data=concerto_in.data,
        capacidade=concerto_in.capacidade
    )
    return 201, concerto

@api.delete("/concertos/{concerto_id}", response={204: None, 404: ErrorSchema}, tags=["Concertos"])
def deletar_concerto(request, concerto_id: int):
    try:
        concerto = Concerto.objects.get(id=concerto_id)
        concerto.delete()
        return 204, None
    except Concerto.DoesNotExist:
        return 404, {"detail": "Concerto não encontrado"}
    
@api.put("/concertos/{concerto_id}", response=ConcertoOut, tags=["Concertos"])
def atualizar_concerto(request, concerto_id: int, concerto_in: ConcertoIn):
    try:
        concerto = Concerto.objects.get(id=concerto_id)
    except Concerto.DoesNotExist:
        return 404, {"detail": "Concerto não encontrado"}

    try:
        banda = Banda.objects.get(id=concerto_in.banda_id)
    except Banda.DoesNotExist:
        return 404, {"detail": "Banda não encontrada"}

    concerto.banda = banda
    concerto.local = concerto_in.local
    concerto.data = concerto_in.data
    concerto.capacidade = concerto_in.capacidade
    concerto.save()
    return concerto

@api.patch("/concertos/{concerto_id}/atribuir_banda/{banda_id}", response=ConcertoOut, tags=["Concertos"])
def atribuir_banda(request, concerto_id: int, banda_id: int):
    try:
        concerto = Concerto.objects.get(id=concerto_id)
        banda = Banda.objects.get(id=banda_id)
        concerto.banda = banda
        concerto.save()
        return concerto
    except Concerto.DoesNotExist:
        return 404, {"detail": "Concerto não encontrado"}
    except Banda.DoesNotExist:
        return 404, {"detail": "Banda não encontrada"}


#BANDAS

@api.get("/bandas", response=list[BandaOut], tags=["Bandas"])
def listar_bandas(request):
    return Banda.objects.all()

@api.post("/bandas",response={201: BandaOut,400: ErrorSchema},tags=["Bandas"])
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
    
    try:
        banda = Banda.objects.get(id=banda_id)
        
        for attr, value in banda_in.dict().items():
            setattr(banda, attr, value)
        
    except Banda.DoesNotExist:
        return 404, {"detail": "Banda não encontrada"}

    banda.save()
    return banda


@api.get("/bandas/{banda_id}/detalhes", response=BandaDetail, tags=["Bandas"])
def detalhar_banda(request, banda_id: int):
    try:
        # prefetch_related porque concertos e musicos são relações reversas/ManyToMany
        banda = Banda.objects.prefetch_related(
            "concertos",
            "musicos"
        ).get(id=banda_id)

        return banda

    except Banda.DoesNotExist:
        return 404, {"detail": "Banda não encontrada"}
    
@api.patch("/bandas/{banda_id}/atribuir_musico/{musico_id}", response=BandaOut, tags=["Bandas"])
def atribuir_musico(request, banda_id: int, musico_id: int):
    try:
        banda = Banda.objects.get(id=banda_id)
        musico = Musico.objects.get(id=musico_id)
        banda.musicos.add(musico)
        banda.save()
        return banda
    except Banda.DoesNotExist:
        return 404, {"detail": "Banda não encontrada"}
    except Musico.DoesNotExist:
        return 404, {"detail": "Músico não encontrado"}

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

@api.delete("/musicos/{musico_id}", response={204: None, 404: ErrorSchema}, tags=["Musicos"])
def deletar_musico(request, musico_id: int):
    try:
        musico = Musico.objects.get(id=musico_id)
        musico.delete()
        return 204, None
    except Musico.DoesNotExist:
        return 404, {"detail": "Músico não encontrado"}
    
@api.put("/musicos/{musico_id}", response=MusicoOut, tags=["Musicos"])
def atualizar_musico(request, musico_id: int, musico_in: MusicoIn):
    musico = Musico.objects.get(id=musico_id)

    for attr, value in musico_in.dict().items():
        setattr(musico, attr, value)

    musico.save()
    return musico

    
@api.patch("/musicos/{musico_id}/atribuir_instrumento/{instrumento_id}", response=MusicoOut, tags=["Musicos"])
def atribuir_instrumento(request, musico_id: int, instrumento_id: int):
    try:
        musico = Musico.objects.get(id=musico_id)
        instrumento = Instrumento.objects.get(id=instrumento_id)
        musico.instrumentos.add(instrumento)
        musico.save()
        return musico
    except Musico.DoesNotExist:
        return 404, {"detail": "Músico não encontrado"}
    except Instrumento.DoesNotExist:
        return 404, {"detail": "Instrumento não encontrado"}
    
@api.get("/musicos/{musico_id}/detalhes", response=MusicoOut, tags=["Musicos"])
def detalhar_musico(request, musico_id: int):
    try:

        # prefetch_related porque instrumentos é ManyToMany
        musico = Musico.objects.prefetch_related(
            "instrumentos"
        ).get(id=musico_id)

        return musico

    except Musico.DoesNotExist:
        return 404, {"detail": "Músico não encontrado"}


#INSTRUMENTOS

@api.get("/instrumentos", 
        response=list[InstrumentoOut], 
        tags=["Instrumentos"])

def listar_instrumentos(request):
    return Instrumento.objects.all()

@api.get("/instrumentos/{instrumento_id}/detalhes", response=InstrumentoOut, tags=["Instrumentos"])
def detalhar_instrumento(request, instrumento_id: int):
    try:
        # prefetch_related porque instrumentos <-> musico é ManyToMany
        instrumento = Instrumento.objects.prefetch_related(
            "musicos"
        ).get(id=instrumento_id)

        return instrumento

    except Instrumento.DoesNotExist:
        return 404, {"detail": "Instrumento não encontrado"}

@api.post("/instrumentos", response=InstrumentoOut, tags=["Instrumentos"])
def criar_instrumento(request, instrumento_in: InstrumentoIn):
    if Instrumento.objects.filter(nome=instrumento_in.nome).exists():
        return 400, {"detail": "Já existe um instrumento com esse nome"}

    instrumento = Instrumento.objects.create(**instrumento_in.dict())
    return 201, instrumento

@api.delete("/instrumentos/{instrumento_id}", response={204: None, 404: ErrorSchema}, tags=["Instrumentos"])
def deletar_instrumento(request, instrumento_id: int):
    try:
        instrumento = Instrumento.objects.get(id=instrumento_id)
        instrumento.delete()
        return 204, None
    except Instrumento.DoesNotExist:
        return 404, {"detail": "Instrumento não encontrado"}

@api.put("/instrumentos/{instrumento_id}", response=InstrumentoOut, tags=["Instrumentos"])
def atualizar_instrumento(request, instrumento_id: int, instrumento_in: InstrumentoIn):
    instrumento = Instrumento.objects.get(id=instrumento_id)

    for attr, value in instrumento_in.dict().items():
        setattr(instrumento, attr, value)

    instrumento.save()
    return instrumento




