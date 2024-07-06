from graphene import relay, Int, String, List, ObjectType, Schema, Argument
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from sqlalchemy import or_
from graphene import Argument
import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
from models.canoa import Canoa as CanoaDBmodel


# Definição de tipos GraphQL usando SQLAlchemyObjectType
class CanoaSchemaGraphQL(SQLAlchemyObjectType):
    class Meta:
        model = CanoaDBmodel
        #interfaces = (relay.Node,)

    # Mapeamento de campos
    idcanoa = Int(source='id_canoa')  # Mapeando idCanoa para id_canoa no modelo SQLAlchemy
    #nome = String(source='nome') 
    #tipo = String(source='tipo') 
    #dono = String(source='dono') 



# Definição de consultas GraphQL

class Query(ObjectType):
    canoas = List(CanoaSchemaGraphQL, tipos=List(String), local=String())

    def resolve_canoas(self, info, tipos=None, local=None):
        query = CanoaSchemaGraphQL.get_query(info)  # SQLAlchemy query

        if tipos is not None:
            query = query.filter(CanoaDBmodel.tipo.in_(tipos))    

        if local:
            # Criar uma condição OR para buscar em qualquer um dos 4 campos
            query = query.filter(
                or_(
                    CanoaDBmodel.estado.like(f"%{local}%"),
                    CanoaDBmodel.municipio.like(f"%{local}%"),
                    CanoaDBmodel.bairro.like(f"%{local}%"),
                    CanoaDBmodel.referencia.like(f"%{local}%")
                )
            )

        return query.all()



schema = Schema(query=Query)