from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from flask_graphql import GraphQLView
from sqlalchemy.exc import IntegrityError


from models import Session
from models.canoa import Canoa

from schemas import *
from logger import logger
from schemas_graphQL import schema

from flask_cors import CORS

info = Info(title="VAAlugar-MS-canoas", version="0.1.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
criacao_canoa_tag = Tag(name="Criação de Canoa", description="Registro de canoas para locação")
exclusao_canoa_tag = Tag(name="Exclusão de Canoa", description="Exclusão de canoas para locação")
atualizacao_avaliacao_canoa_tag = Tag(name="Atualização de Avaliação de Canoa", description="Atualização de Avaliação de Canoa")
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")





@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação."""
    return redirect('/openapi')







@app.post('/criar', tags=[criacao_canoa_tag],
          responses={"200": SchemaVisualizacaoCanoa, "409": SchemaMensagemErro, "400": SchemaMensagemErro})
def cria_canoa(form: SchemaCriacaoCanoa):
    """Cria uma canoa

    Retorna uma representação da canoa criada. 
    """
    logger.debug(f"Recebido dados para criação de canoa: {form}")
    print(f"Recebido dados para criação de canoa: {form}")
    canoa = Canoa(
        nome=form.nome, 
        tipo=form.tipo, 
        dono=form.dono,
        estado=form.estado,
        municipio=form.municipio,
        bairro=form.bairro,
        referencia=form.referencia,
        latitude=form.latitude,
        longitude=form.longitude,
        qtde_avaliacoes=0


    )
    #logger.debug(f"Canoa criada: {canoa}")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando reserva
        session.add(canoa)
        # efetivando o comando de criação da reserva na tabela
        session.commit()
        logger.debug(f"Reserva persistida no banco de dados: {canoa}")
        return apresenta_canoa(canoa), 200
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = f"Não foi possível criar canoa : {e}"
        logger.warning(f"Erro ao criar reserva, {error_msg}")
        return {"message": error_msg}, 400











@app.delete('/excluir', tags=[exclusao_canoa_tag],
            responses={"200": SchemaVisualizacaoCanoa, "404": SchemaMensagemErro, "400": SchemaMensagemErro})
def exclui_canoa(form: SchemaExclusaoCanoa):
    """Exclui uma canoa

    Retorna uma representação da canoa excluída. 
    """
    logger.debug(f"Recebido dados para exclusão de canoa: {form}")
    try:
        # criando conexão com a base
        session = Session()
        # buscando a canoa a ser excluída
        canoa = session.query(Canoa).filter_by(id_canoa=form.id_canoa).first()
        if canoa is None:
            error_msg = "Canoa não encontrada"
            logger.warning(f"Erro ao excluir canoa, {error_msg}")
            return {"message": error_msg}, 404

        logger.debug(f"Canoa encontrada: {canoa}")

        # excluindo a canoa
        session.delete(canoa)
        # efetivando a exclusão no banco de dados
        session.commit()
        logger.debug(f"Canoa excluída do banco de dados: {canoa}")
        return apresenta_canoa(canoa), 200
    except Exception as e:
        # caso um erro fora do previsto
        session.rollback()  # reverte quaisquer mudanças no banco de dados
        error_msg = f"Não foi possível excluir a canoa: {e}"
        logger.warning(f"Erro ao excluir canoa, {error_msg}")
        return {"message": error_msg}, 400
    finally:
        session.close()




@app.patch('/atualizaravaliacao', tags=[atualizacao_avaliacao_canoa_tag],
            responses={"200": SchemaVisualizacaoCanoa, "404": SchemaMensagemErro, "400": SchemaMensagemErro})
def atualiza_avaliacao_canoa(body: SchemaAtualizacaoAvaliacao):
    """Atualiza os valores referentes a avaliações recebidas pela canoa: quantidade de avaliações e média das respostas.

    Retorna uma representação atualizada da canoa. 
    """
    logger.debug(f"Recebido dados para atualização de canoa: {body}")
    print(f"Recebido dados para atualização de canoa: {body}")
    try:
        # criando conexão com a base
        session = Session()
        # buscando a canoa a ser excluída
        canoa = session.query(Canoa).filter_by(id_canoa=body.id_canoa).first()
        if canoa is None:
            error_msg = "Canoa não encontrada"
            logger.warning(f"Erro ao excluir canoa, {error_msg}")
            return {"message": error_msg}, 404

        logger.debug(f"Canoa encontrada: {canoa}")

        # Atualizando os campos relevantes
        canoa.qtde_avaliacoes = body.qtde_avaliacoes
        canoa.media_avaliacoes = body.media_avaliacoes


        # Commitando as mudanças no banco de dados
        session.commit()
        logger.debug(f"Dados de avaliação da canoa atualizados: {canoa}")
        print(f"Dados de avaliação da canoa atualizados: {canoa}")


        return apresenta_canoa(canoa), 200
    

    except Exception as e:
        # caso um erro fora do previsto
        session.rollback()  # reverte quaisquer mudanças no banco de dados
        error_msg = f"Não foi possível excluir a canoa: {e}"
        logger.warning(f"Erro ao excluir canoa, {error_msg}")
        return {"message": error_msg}, 400
    
    
    finally:
        session.close()





# Configuração do endpoint GraphQL
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True  # Habilita a interface GraphiQL para testar queries
    )
)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
