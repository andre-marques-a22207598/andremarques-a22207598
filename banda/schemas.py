from ninja import Schema

class ErrorSchema(Schema):
    detail: str

class BandaIn(Schema):
    nome: str
    genero: str
    ano_formacao: int
    
class BandaOut(BandaIn):
    id: int

class InstrumentoIn(Schema):
    nome: str
    tipo: str
    naipe: str
    
class InstrumentoOut(InstrumentoIn):
    id: int
    
class MusicoIn(Schema):
    nome: str
    idade: int

class MusicoOut(MusicoIn):
    id: int
    instrumentos: list[InstrumentoOut] 

class ConcertoIn(Schema):
    banda_id: int
    local: str
    data: str  # ISO format date
    capacidade: int

class ConcertoOut(ConcertoIn):
    id: int
    
class BandaDetail(BandaOut):
    concertos: list[ConcertoOut]