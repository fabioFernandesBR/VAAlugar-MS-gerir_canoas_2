'''
Criei este arquivo init dentro da pasta database e aqui vou colocar 
tanto as funções de uso do banco de dados quanto os modelos SQLAlchemy.
'''

from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import (create_engine)
import os

from sqlalchemy.ext.declarative import declarative_base

# Classe Base
### essa função vem do SQLAlchemy, e cria a classe Base, que será usada depois
### como classe-mãe das classes que representarão tabelas do banco de dados.
Base = declarative_base() 


# Conectando ao banco de dados
db_path = "database/"

## url de acesso ao banco (essa é uma url de acesso ao sqlite local)
db_url = 'sqlite:///%s/canoas.sqlite' % db_path

# cria a engine de conexão com o banco
engine = create_engine(db_url, echo=True)

# Instancia um criador de seção com o banco
Session=scoped_session(sessionmaker(bind=engine))

Base.query = Session.query_property()  # cria na classe Base uma propriedade query

from models.canoa import Canoa

# Cria todas as tabelas no banco de dados
Base.metadata.create_all(engine)      