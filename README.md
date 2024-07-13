# VAAlugar-MS-canoas-2

Repositório do projeto VA'Alugar em Microsserviços (MS).Para mais informações sobre este projeto, consultar o readme do repositório Gateway: https://github.com/fabioFernandesBR/VAAlugar-MS-gateway/blob/main/README.md.




Este MS executa tarefas de gestão das canoas, tais como criar, excluir, atualizar e consultar canoas.
Em relação à versão anterior:
- a base de dados agora inclui campos para localização e geolocalização, como estado, município, bairro e referência e latitude e longitude. Também foram incluídos campos referentes às avaliações recebidas, tais como quantidade de avaliações e média das avaliações.
- a pesquisa pelo GraphQL toma apenas 1 string e faz as busca nas 4 variáveis de localização.
- foi adicionada uma rota para atualização das informações sobre as avaliações.

### ATENÇÃO: rodar na porta 5002.



## Esquema de Fluxo de informações:
Disponibiliza as seguintes rota para comunicação via REST:

### /criar: 
usando o método POST. Ao chamar esta rota, informar via JSON. O MS vai registrar no banco de dados SQLite (exclusivo deste MS) e retornar a confirmação da criação da canoa ou algum erro.

/excluir: usando o método DELETE. Ao chamar esta rota, informar via JSON conforme definido na seção Parâmetros. O MS vai excluir do banco de dados SQLite e retornar a confirmação da exclusão da canoa ou algum erro.

/atualizaravaliacao: usando o método PATCH. Ao chamar esta rota, informar via JSON conforme definido na seção Parâmetros. O MS vai atualizar o banco de dados SQLite e retornar a a representação da canoa com os novos valores ou algum erro.

Com a rota /graphql, diferentes parâmetros podem ser passados via GraphQL, para consulta das canoas disponíveis:
- query se chama canoas.
- 2 critérios de busca são habilitados: local e tipos. Local é string, e pesquisa nos campos relacionados à localização: estado, município, bairro e referência. Basta que 1 desses campos contenha a string pesquisada e a canoa será retornada pela query. Tipos é habilitado como lista, de modo que pode-se pesquisar por mais de um valor, como ["OC1", "OC2"], por exemplo.
- Os tipos são as características das canoas, como OC2, OC4 e OC6. São strings e devem ser passadas como lista.


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
