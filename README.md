# VAAlugar-MS-canoas-2

Repositório do projeto VA'Alugar em Microsserviços (MS) para a gestão das canoas. Para mais informações sobre este projeto, consultar o readme do repositório Gateway: https://github.com/fabioFernandesBR/VAAlugar-MS-gateway/blob/main/README.md.


Este MS executa tarefas de gestão das canoas, tais como criar, excluir, atualizar e consultar canoas.
Em relação à versão anterior:
- a base de dados agora inclui campos para localização e geolocalização, como estado, município, bairro e referência e latitude e longitude. Também foram incluídos campos referentes às avaliações recebidas, tais como quantidade de avaliações e média das avaliações.
- a pesquisa pelo GraphQL toma apenas 1 string e faz as busca nas 4 variáveis de localização.
- foi adicionada uma rota para atualização das informações sobre as avaliações.

### ATENÇÃO: rodar na porta 5002.


## Esquema de Fluxo de informações:
Disponibiliza as seguintes rota para comunicação via REST:

### /criar: 
usando o método POST. Ao chamar esta rota, passar um dicionário com os parâmetros. O MS vai registrar no banco de dados SQLite (exclusivo deste MS) e retornar a confirmação da criação da canoa ou algum erro.
Modelo do dicionário:
data = {
    'nome': 'string',
    'tipo': 'string',
    'dono': 'string',
    'estado': 'string',
    'municipio': 'string',
    'bairro': 'string',  # Este campo é opcional
    'referencia': 'string',  # Este campo é opcional
    'latitude': float,  # Este campo é opcional
    'longitude': float  # Este campo é opcional
}.

Exemplo:

data = {
    'nome': 'Serena',
    'tipo': 'OC1',
    'dono': 'Fábio',
    'estado': 'RJ',
    'municipio': 'Resende',
    'bairro': 'Zona Rural',  # Este campo é opcional
    'referencia': 'Represa do Funil, Clube Náutico',  # Este campo é opcional
    'latitude': -23.55052,  # Este campo é opcional
    'longitude': -46.633308  # Este campo é opcional
}.

O retorno é uma variável JSON, como no exemplo:
{
  "bairro": "Glória",
  "dono": "Fabio",
  "estado": "RJ",
  "id_canoa": 1,
  "latitude": -22.922477,
  "longitude": -43.385915,
  "media_avaliacoes": 0,
  "municipio": "Rio de Janeiro",
  "nome": "E Ala E",
  "qtde_avaliacoes": 0,
  "referencia": "Aterro do Flamengo",
  "tipo": "OC2"
}

Observe que em relação aos parâmetros passados para criação da canoa, no retorno há o acréscimo de 3 parâmetros: id_canoa, qtde_avaliacoes e media_avaliacoes. Por default, no momento da criação da canos, os  parâmetros qtde_avaliacoes e media_avaliacoes sempre retornarão 0, já que a canoa recém criada ainda não tem nenhuma avaliação. Como esse é o esquema padrão de retorno das operações de consulta, exclusão e atualização, temos essa redundância de informação. No futuro, pretendo implementar operações de mutation em rota graphql para que o fluxo de informação seja mais limpo.


### /excluir: 
usando o método DELETE. Ao chamar esta rota, passar um dicionário com o parâmetro. O MS vai excluir do banco de dados SQLite e retornar a confirmação da exclusão da canoa ou algum erro.

Modelo do dicionário:
data = {
    'id_canoa': int
    }.

O retorno é um JSON do mesmo padrão de retorno da rota /criar. Exemplo:
{
  "bairro": "Glória",
  "dono": "Fabio",
  "estado": "RJ",
  "id_canoa": 1,
  "latitude": -22.922477,
  "longitude": -43.385915,
  "media_avaliacoes": 0,
  "municipio": "Rio de Janeiro",
  "nome": "E Ala E",
  "qtde_avaliacoes": 0,
  "referencia": "Aterro do Flamengo",
  "tipo": "OC2"
}

### /atualizaravaliacao: 
Usando o método PATCH. Ao chamar esta rota, passar um dicionário com os parâmetros. O MS vai atualizar o banco de dados SQLite e retornar a a representação da canoa com os novos valores ou algum erro. O retorno segue o padrão das rotas anteriores:

Modelo do dicionário:
data = {
    'id_canoa': int,
    'qtde_avaliacoes': int,
    'media_avaliacoes': float
}.

Exemplo:

data = {
    'id_canoa': 1,
    'qtde_avaliacoes': 8,
    'media_avaliacoes': 9.25
}.

O retorno é uma variável JSON, como no exemplo:
{
  "bairro": "Glória",
  "dono": "Fabio",
  "estado": "RJ",
  "id_canoa": 1,
  "latitude": -22.922477,
  "longitude": -43.385915,
  "media_avaliacoes": 9.25,
  "municipio": "Rio de Janeiro",
  "nome": "E Ala E",
  "qtde_avaliacoes": 8,
  "referencia": "Aterro do Flamengo",
  "tipo": "OC2"
}

### Consulta via graphql
Com a rota /graphql, diferentes parâmetros podem ser passados via GraphQL, para consulta das canoas disponíveis:
- query se chama canoas.
- 2 critérios de busca são habilitados: local e tipos. Local é string, e pesquisa nos campos relacionados à localização: estado, município, bairro e referência. Basta que 1 desses campos contenha a string pesquisada e a canoa será retornada pela query. Tipos é habilitado como lista, de modo que pode-se pesquisar por mais de um valor, como ["OC1", "OC2"], por exemplo.
- Os tipos são as características das canoas, como OC2, OC4 e OC6. São strings e devem ser passadas como lista.

Exemplos:

{query: canoas {
  nome
  tipo
  dono
  estado
  municipio
  bairro
  referencia
  latitude
  longitude
  mediaAvaliacoes
  qtdeAvaliacoes
  idcanoa
}}

retorna todas as canoas:

{
  "data": {
    "query": [
      {
        "nome": "E Ala E",
        "tipo": "OC2",
        "dono": "Fábio",
        "estado": "RJ",
        "municipio": "Rio de Janeiro",
        "bairro": "Recreio",
        "referencia": "Posto 12 Pedra do Pontal",
        "latitude": null,
        "longitude": null,
        "mediaAvaliacoes": 8.777777777777779,
        "qtdeAvaliacoes": 9,
        "idcanoa": 1
      },
      {
        "nome": "Aia Ka La",
        "tipo": "OC4",
        "dono": "Fábio",
        "estado": "RJ",
        "municipio": "Rio de Janeiro",
        "bairro": "Guaratiba",
        "referencia": "Restinga da Marambaia",
        "latitude": null,
        "longitude": null,
        "mediaAvaliacoes": 9,
        "qtdeAvaliacoes": 2,
        "idcanoa": 4
      },
      {
        "nome": "I Ka Moana",
        "tipo": "OC2",
        "dono": "Vanessa",
        "estado": "RJ",
        "municipio": "Niterói",
        "bairro": "Itaipu",
        "referencia": "Rio de Janeiro RJ Niteroi Região Oceânica Itaipu",
        "latitude": null,
        "longitude": null,
        "mediaAvaliacoes": null,
        "qtdeAvaliacoes": 0,
        "idcanoa": 5
      },
      {
        "nome": "Rainha da Baía",
        "tipo": "OC2",
        "dono": "Fábio",
        "estado": "RJ",
        "municipio": "Niterói",
        "bairro": "Icaraí",
        "referencia": "Praia de Icaraí",
        "latitude": null,
        "longitude": null,
        "mediaAvaliacoes": 8.9,
        "qtdeAvaliacoes": 2,
        "idcanoa": 6
      },
      {
        "nome": "Amora",
        "tipo": "OC2",
        "dono": "Vanessa",
        "estado": "RJ",
        "municipio": "Rio de Janeiro",
        "bairro": "Barra",
        "referencia": "Praia dos Amores",
        "latitude": null,
        "longitude": null,
        "mediaAvaliacoes": 8.95,
        "qtdeAvaliacoes": 2,
        "idcanoa": 7
      },
      {
        "nome": "do Pontal",
        "tipo": "OC6",
        "dono": "Vitinho",
        "estado": "Rio de Janeiro",
        "municipio": "Rio de Janeiro",
        "bairro": null,
        "referencia": "Praia do Pontal, posto 12",
        "latitude": null,
        "longitude": null,
        "mediaAvaliacoes": 9.9,
        "qtdeAvaliacoes": 1,
        "idcanoa": 8
      }
    ]
  }
}

{query: canoas {
  nome
  tipo
  latitude
  longitude
  mediaAvaliacoes
  qtdeAvaliacoes
  idcanoa
}}

retorna todas as canoas, porém um conjunto menor de informações:

{
  "data": {
    "query": [
      {
        "nome": "E Ala E",
        "tipo": "OC2",
        "latitude": null,
        "longitude": null,
        "mediaAvaliacoes": 8.777777777777779,
        "qtdeAvaliacoes": 9,
        "idcanoa": 1
      },
      {
        "nome": "Aia Ka La",
        "tipo": "OC4",
        "latitude": null,
        "longitude": null,
        "mediaAvaliacoes": 9,
        "qtdeAvaliacoes": 2,
        "idcanoa": 4
      },
      {
        "nome": "I Ka Moana",
        "tipo": "OC2",
        "latitude": null,
        "longitude": null,
        "mediaAvaliacoes": null,
        "qtdeAvaliacoes": 0,
        "idcanoa": 5
      },
      {
        "nome": "Rainha da Baía",
        "tipo": "OC2",
        "latitude": null,
        "longitude": null,
        "mediaAvaliacoes": 8.9,
        "qtdeAvaliacoes": 2,
        "idcanoa": 6
      },
      {
        "nome": "Amora",
        "tipo": "OC2",
        "latitude": null,
        "longitude": null,
        "mediaAvaliacoes": 8.95,
        "qtdeAvaliacoes": 2,
        "idcanoa": 7
      },
      {
        "nome": "do Pontal",
        "tipo": "OC6",
        "latitude": null,
        "longitude": null,
        "mediaAvaliacoes": 9.9,
        "qtdeAvaliacoes": 1,
        "idcanoa": 8
      }
    ]
  }
}


{query: canoas (local: "Niterói") {
  nome
  tipo
  latitude
  longitude
  mediaAvaliacoes
  qtdeAvaliacoes
  idcanoa
}}

retorna

{
  "data": {
    "query": [
      {
        "nome": "I Ka Moana",
        "tipo": "OC2",
        "latitude": null,
        "longitude": null,
        "mediaAvaliacoes": null,
        "qtdeAvaliacoes": 0,
        "idcanoa": 5
      },
      {
        "nome": "Rainha da Baía",
        "tipo": "OC2",
        "latitude": null,
        "longitude": null,
        "mediaAvaliacoes": 8.9,
        "qtdeAvaliacoes": 2,
        "idcanoa": 6
      }
    ]
  }
}

e 

{query: canoas (local: "RJ", tipos: ["OC4"]) {
  nome
  tipo
  latitude
  longitude
  mediaAvaliacoes
  qtdeAvaliacoes
  idcanoa
}}

retorna

{
  "data": {
    "query": [
      {
        "nome": "Aia Ka La",
        "tipo": "OC4",
        "latitude": null,
        "longitude": null,
        "mediaAvaliacoes": 9,
        "qtdeAvaliacoes": 2,
        "idcanoa": 4
      }
    ]
  }
}

e por exemplo:
{query: canoas (local: "RJ", tipos: ["OC2", "OC4"]) {
  nome
  tipo
  latitude
  longitude
  mediaAvaliacoes
  qtdeAvaliacoes
  idcanoa
}}

retorna:

{
  "data": {
    "query": [
      {
        "nome": "E Ala E",
        "tipo": "OC2",
        "latitude": null,
        "longitude": null,
        "mediaAvaliacoes": 8.777777777777779,
        "qtdeAvaliacoes": 9,
        "bairro": "Recreio",
        "municipio": "Rio de Janeiro",
        "referencia": "Posto 12 Pedra do Pontal"
      },
      {
        "nome": "Aia Ka La",
        "tipo": "OC4",
        "latitude": null,
        "longitude": null,
        "mediaAvaliacoes": 9,
        "qtdeAvaliacoes": 2,
        "bairro": "Guaratiba",
        "municipio": "Rio de Janeiro",
        "referencia": "Restinga da Marambaia"
      },
      {
        "nome": "I Ka Moana",
        "tipo": "OC2",
        "latitude": null,
        "longitude": null,
        "mediaAvaliacoes": null,
        "qtdeAvaliacoes": 0,
        "bairro": "Itaipu",
        "municipio": "Niterói",
        "referencia": "Rio de Janeiro RJ Niteroi Região Oceânica Itaipu"
      },
      {
        "nome": "Rainha da Baía",
        "tipo": "OC2",
        "latitude": null,
        "longitude": null,
        "mediaAvaliacoes": 8.9,
        "qtdeAvaliacoes": 2,
        "bairro": "Icaraí",
        "municipio": "Niterói",
        "referencia": "Praia de Icaraí"
      },
      {
        "nome": "Amora",
        "tipo": "OC2",
        "latitude": null,
        "longitude": null,
        "mediaAvaliacoes": 8.95,
        "qtdeAvaliacoes": 2,
        "bairro": "Barra",
        "municipio": "Rio de Janeiro",
        "referencia": "Praia dos Amores"
      }
    ]
  }
}


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
Considere as seguintes opções: instalar apenas este microsserviço, diretamente do IDE, como Visual Studio Code; ou instalar todos os microsserviços via Docker Compose.

### Para rodar este MS diretamente do IDE.
No Windows:
1. Faça o clone deste repositório para sua máquina.
2. Crie um ambiente virtual, com o comando "Python -m venv env", diretamente no terminal.
3. Em seguida ative o ambiente virtual, com o comando ".\env\Scripts\activate".
4. Instale as dependências necessárias com o comando "pip install -r requirements.txt".
5. Execute com o comando "flask run --host 0.0.0.0 --port 5002"
Para Mac ou Linux, a lógica é a mesma, mas faça as adaptações necessárias.

### Como executar através do Docker Compose
Para que os microsserviços interajam, é necessário que todos estejam rodando. A forma mais fácil de instalar e executar todos está descrita no link:
https://github.com/fabioFernandesBR/VAAlugar-Docker-Compose/blob/main/README.md
