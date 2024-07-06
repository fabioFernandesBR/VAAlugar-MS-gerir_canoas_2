from sqlalchemy.ext.declarative import declarative_base
from models import Session

# Classe Base
### essa função vem do SQLAlchemy, e cria a classe Base, que será usada depois
### como classe-mãe das classes que representarão tabelas do banco de dados.
Base = declarative_base() 
Base.query = Session.query_property()  # cria na classe Base uma propriedade query