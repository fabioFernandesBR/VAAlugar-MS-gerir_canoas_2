from pydantic import BaseModel
from typing import Optional, List




# BaseModel é a classe base do Pydantic.
# As classes a seguir são modelos de dados baseadas em Pydantic.


# Operações que queremos implementar:
## Criar canoa
## Deletar canoa
## Consultar canoa, informando dados como lista de locais, dono ou tipo de canoa

class SchemaCriacaoCanoa(BaseModel):
    """ 
    Define como uma nova canoa a ser criada deve ser representada. 
    Fluxo: do usuário para a API. 

    Método POST
    """
    nome: str = "E Ala E"
    tipo: str = "OC2"
    dono: str = "Fábio"
    estado: str = "RJ"
    municipio: str = "Rio de Janeiro"
    bairro: Optional[str] = None
    referencia: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class SchemaExclusaoCanoa(BaseModel):
    """ 
    Define como uma canoa a ser excluída deve ser representada. 
    Fluxo: do usuário para a API. 

    Método DELETE
    """
    id_canoa: int = 1


class SchemaAtualizacaoAvaliacao(BaseModel):
    """ 
    Define como informar nova média e quantidade de avaliações. 
    Fluxo: do usuário para a API. 

    Método PATCH
    """
    id_canoa: int
    qtde_avaliacoes: int
    media_avaliacoes: float




class SchemaVisualizacaoCanoa(BaseModel):
    """ 
    Define como uma nova canoa recém criada ou uma canoa recém excluída deve ser representada. 
    Fluxo: da API para o usuário.
    """
    id_canoa: int = 1
    nome: str = "E Ala E"
    tipo: str = "OC2"
    dono: str = "Fabio"
    qtde_avaliacoes: int
    media_avaliacoes: float
    estado: Optional[str] = "RJ" 
    municipio: Optional[str] = "Rio de Janeiro"
    bairro: Optional[str] = "Glória"
    referencia: Optional[str] = "Aterro do Flamengo"
    latitude: Optional[float] = -22.922477
    longitude: Optional[float] = -43.385915



def apresenta_canoa(canoa):
    """Retorna uma representação da canoa."""
    return {
        "id_canoa": canoa.id_canoa,
        "nome": canoa.nome,
        "tipo": canoa.tipo,
        "media de avaliações": canoa.media_avaliacoes,
        "quantidade de avaliações": canoa.qtde_avaliacoes,
        "estado": canoa.estado,
        "municipio": canoa.municipio,
        "bairro": canoa.bairro,
        "latitude": canoa.latitude,
        "longitude": canoa.longitude,
        "referencia": canoa.referencia,
        "dono": canoa.dono
    }
