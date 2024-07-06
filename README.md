# VAAlugar-MS-canoas-2

Repositório do projeto de Microsserviço (MS) que executa tarefa de gestão das canoas, tais como criar, excluir, atualizar e consultar canoas.
Em relação à versão anterior:
- a base de dados agora inclui campos para localização e geolocalização, como estado, município, bairro e referência e latitude e longitude. Também foram incluídos campos referentes às avaliações recebidas, tais como quantidade de avaliações e média das avaliações.
- a pesquisa pelo GraphQL toma apenas 1 string e faz as busca nas 4 variáveis de localização.
- foi adicionada uma rota para atualização das informações sobre as avaliações.

ATENÇÃO: Docker configurado para rodar na porta 5002.

O que este microsserviço faz
Este MS gerencia as canoas.

Disponibiliza as seguintes rota para comunicação via REST:
/criar: usando o método POST. Ao chamar esta rota, informar via JSON conforme definido na seção Parâmetros. O MS vai registrar no banco de dados SQLite (exclusivo deste MS) e retornar a confirmação da criação da canoa ou algum erro.

/excluir: usando o método DELETE. Ao chamar esta rota, informar via JSON conforme definido na seção Parâmetros. O MS vai excluir do banco de dados SQLite e retornar a confirmação da exclusão da canoa ou algum erro.

/atualizaravaliacao: usando o método PATCH. Ao chamar esta rota, informar via JSON conforme definido na seção Parâmetros. O MS vai atualizar o banco de dados SQLite e retornar a a representação da canoa com os novos valores ou algum erro.

Com a rota /graphql, diferentes parâmetros podem ser passados via GraphQL, para consulta das canoas disponíveis:
- query se chama canoas.
- 2 critérios de busca são habilitados: local e tipos. Local é string, e pesquisa nos campos relacionados à localização: estado, município, bairro e referência. Basta que 1 desses campos contenha a string pesquisada e a canoa será retornada pela query. Tipos é habilitado como lista, de modo que pode-se pesquisar por mais de um valor, como ["OC1", "OC2"], por exemplo.
- Os tipos são as características das canoas, como OC2, OC4 e OC6. São strings e devem ser passadas como lista.



## Parâmetros






## Criação do banco de dados: 1 tabela!!
CREATE TABLE canoas (
    id_canoa         INTEGER PRIMARY KEY AUTOINCREMENT,
    nome             TEXT,
    tipo             TEXT,
    dono             TEXT,
    estado           TEXT,
    municipio        TEXT,
    bairro           TEXT,
    referencia       TEXT,
    latitude         NUMERIC,
    longitude        NUMERIC,
    media_avaliacoes REAL,
    qtde_avaliacoes  INTEGER
);

## Instalação
Para instalar: use o arquivo requirements.txt para instalar os módulos. No windows: pip install -r requirements.txt Recomendo instalação em um ambiente virtual

Para executar localmente, em ambiente Windows: flask run --host 0.0.0.0 --port 5000 --reload

## Como executar através do Docker
Certifique-se de ter o Docker instalado e em execução em sua máquina.

Navegue até o diretório que contém o Dockerfile e o requirements.txt no terminal. Execute como administrador o seguinte comando para construir a imagem Docker:

docker build -t ms-canoas-2 .
Uma vez criada a imagem, para executar o container basta executar, como administrador, seguinte o comando:

docker run -p 5002:5002 ms-canoas-2

Uma vez executando, para acessar a API, basta abrir o http://localhost:5002/#/ no navegador.
