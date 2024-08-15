CREATE TYPE FORMA_EXTRACAO AS ENUM ("api","webscrapping","ftp");

CREATE TABLE IF NOT EXISTS dimensao_dado (
  dado_id SERIAL PRIMARY KEY,
  nome_dado VARCHAR(100) NOT NULL,
  topico VARCHAR(50) NOT NULL, --topico do dado, é tambem o nome da tabela que vamos utilizar para carregar os dados
  orgao_fonte VARCHAR(50), -- orgão do governo 
  forma_extracao FORMA_EXTRACAO, --enum para forma de extração dos dados
  fonte_extracao VARCHAR (250), -- fonte dos dados, ou nome da api ou link
  anos_serie_historica INTEGER ARRAY --lista de anos de série histórica que os dados tem
);

CREATE TABLE IF NOT EXISTS dimensao_municipio (
   municipio_id SERIAL PRIMARY KEY,
   
   numero_uf_ibge INTEGER DEFAULT -1, --número da UF segundo o IBGE
   nome_uf VARCHAR(50) NOT NULL, --nome e sigla da UF, esses são obrigatórios 
   sigla_uf VARCHAR(2) NOT NULL,

   numero_regiao_geografica_intermediaria INTEGER DEFAULT -1, --numero de divisões geográficas segundo o IBGE
   nome_regiao_geografica_intermediaria VARCHAR(100) DEFAULT 'n/a',
   
   numero_regiao_geografica_imediata INTEGER DEFAULT -1,
   nome_regiao_geografica_imediata VARCHAR(100) DEFAULT 'n/a',
   
   numero_mesorregiao_geografica INTEGER DEFAULT -1,
   nome_mesorregiao_geografica VARCHAR(100) DEFAULT 'n/a',
   
   numero_microrregiao_geografica INTEGER DEFAULT -1,
   nome_microrregiao_geografica VARCHAR(100) DEFAULT 'n/a',

   codigo_municipio INTEGER NOT NULL CONSTRAINT codigo_munic_7_digitos CHECK (codigo_municipio BETWEEN 1000000 AND 9999999), --código do município do IBGE, um inteiro de 7 dígitos
   nome_municipio VARCHAR(100) NOT NULL,

   nome_regiao_nacional VARCHAR(50) NOT NULL --uma das 5 regiões do brasil
);

CREATE TYPE TIPO_INDICADOR AS ENUM ('principal','adicional');
CREATE TYPE RELEVANCIA_INDICADOR AS ENUM ('alta','media','baixa','n/a');

CREATE TABLE IF NOT EXISTS dimensao_indicador(
  indicador_id SERIAL PRIMARY KEY,
  dimensao VARCHAR(100) NOT NULL,
  subdimensao VARCHAR(100) DEFAULT 'n/a', --subdimensão não é necessário e em vários indicadores ela é nula
  topico VARCHAR(100) NOT NULL, --Tópico não pode ser nulo, pois ele dá nome à tabela que contém os dados
  nome_indicador VARCHAR(150) NOT NULL,
  
  nivel_indicador INTEGER DEFAULT -1, --caso não exista o padrão é -1
  tipo TIPO_INDICADOR DEFAULT 'n/a',
  relevancia RELEVANCIA_INDICADOR DEFAULT 'n/a', --valor caso a relevância não exista
  peso_estatistico INTEGER DEFAULT -1,
  texto_explicativo_indicador TEXT, --texto por conter um parágrafo mais longo
  instituicao_fonte_dados VARCHAR(100) NOT NULL
);

--tabela de junção entre indicador e dados, para modelar a relação many-to-many deles
CREATE TABLE IF NOT EXISTS juncao_dados_indicador (
    dado_id INT,
    indicador_id INT,
    CONSTRAINT fk_dado FOREIGN KEY (dado_id) REFERENCES dimensao_dado(dado_id),
    CONSTRAINT fk_indicador FOREIGN KEY (indicador_id) REFERENCES dimensao_indicador(indicador_id),
    PRIMARY KEY (dado_id, indicador_id) --guarante que a combinação desses dados é única, ou seja não podem existir linhas duplicadas 
);


--query para acessar os dados de um indicador x

--subquery (1) de achar id do indicador
SELECT indicador_id FROM dimensao_indicador
WHERE dimensao_indicador.nome_indicador = 'nome_indicador';

--subquery (2), de achar os ids dos dados
SELECT dado_id FROM juncao_dados_indicador
WHERE juncao_dados_indicador.indicador_id = 'resultado da subquery 1';

--nessa query todos os dados na coluna topico vão ser iguais (devem)
SELECT topico,dado_id,anos_serie_historica FROM 'tabela_subquery2'
INNER JOIN dimensao_dado ON dimensao_dado.dado_id = 'tabela_subquery2'.dado_id;


--combinação das subqueries 1 e 2
SELECT dado_id FROM juncao_dados_indicador
INNER JOIN dimensao_indicador ON dimensao_indicador.indicador_id  = juncao_dados_indicador.indicador_id
WHERE dimensao_indicador.nome_indicador = 'nome_indicador';


--query final 
SELECT topico,dado_id,anos_serie_historica FROM dimensao_dado --começa a query da tabela de dimensões de dados. Seleciona essas 3 colunas
INNER JOIN juncao_dados_indicador on juncao_dados_indicador.dado_id = dimensao_dado.dado_id --inner join com tabela de juncao 
INNER JOIN dimensao_indicador ON dimensao_indicador.indicador_id = juncao_dados_indicador.indicador_id --inner join da tabela de juncao com tabela de indicadores
WHERE dimensao_indicador.nome_indicador = 'nome_indicador'; --filtra pela nome do indicador



--OBS usar queries de inserir com o RETURNING  para pegar a foreign key da inserção e criar a tabela de junção mais fácil
INSERT INTO table_a (column1, column2, ...)
VALUES (value1, value2, ...)
RETURNING pk_column_name;


--Tabelas de fato e queries associadas