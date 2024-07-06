from sqlalchemy import Column, String, Integer, Numeric, REAL
from models import Base


class Canoa(Base):
    __tablename__ = 'canoas'

    id_canoa = Column(Integer, primary_key = True)
    nome = Column(String(50))
    tipo = Column(String(20))
    dono = Column(String(50))
    estado = Column(String(50))
    municipio = Column(String(50))
    bairro = Column(String(50))
    referencia = Column(String(50))
    latitude = Column(Numeric(10,8))
    longitude = Column(Numeric(10,8))
    media_avaliacoes = Column(REAL)
    qtde_avaliacoes = Column(Integer)

    
    def __init__(self, nome, tipo, dono, estado, municipio, bairro = None, referencia = None, latitude = None, longitude = None, qtde_avaliacoes = None, media_avaliacoes = None):
        
        # Cria uma Canoa!

        #Arguments:
        #    nome
        #    tipo
        #    dono
        #    telefone: Integer
        #    local: Integer, referência ao local onde está armazenada
        
        self.nome = nome
        self.tipo = tipo
        self.dono = dono
        
        # Atributos novos - para referenciar localidade
        self.estado = estado
        self.municipio = municipio
        self.bairro = bairro
        self.referencia = referencia
        self.latitude = latitude
        self.longitude = longitude

        # Atributos novos - para informar sobre as avaliacoes
        self.qtde_avaliacoes = qtde_avaliacoes
        self.media_avaliacoes = media_avaliacoes

        