CREATE TYPE FORMA_EXTRACAO AS ENUM ('api','webscrapping','ftp');

CREATE TABLE IF NOT EXISTS dimensao_dado (
  dado_id SERIAL PRIMARY KEY,
  nome_dado VARCHAR(200) NOT NULL,
  topico VARCHAR(50) NOT NULL, --topico do dado, é tambem o nome da tabela que vamos utilizar para carregar os dados
  orgao_fonte VARCHAR(50), -- orgão do governo 
  forma_extracao FORMA_EXTRACAO, --enum para forma de extração dos dados
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


--OBS usar queries de inserir com o RETURNING  para pegar a foreign key da inserção e criar a tabela de junção mais fácil

INSERT INTO table_a (column1, column2, ...)
VALUES (value1, value2, ...)
RETURNING pk_column_name;

--Queries de inserir nas tabelas de dimensão

INSERT INTO dimensao_indicador (
    dimensao,
    subdimensao,
    topico,
    nome_indicador,
    nivel_indicador,
    tipo,
    relevancia,
    peso_estatistico,
    texto_explicativo_indicador,
    instituicao_fonte_dados
) VALUES 
      {values}
RETURNING indicador_id;


INSERT INTO dimensao_dado (
      nome_dado,
      topico,
      orgao_fonte,
      forma_extracao,
      anos_serie_historica
) VALUES 
      {values}
RETURNING dado_id;

INSERT INTO juncao_dados_indicador(dado_id,indicador_id) VALUES 
      {values_str};

INSERT INTO dimensao_municipio (
      numero_uf_ibge,
      nome_uf,
      sigla_uf,
      numero_regiao_geografica_intermediaria,
      nome_regiao_geografica_intermediaria,
      numero_regiao_geografica_imediata,
      nome_regiao_geografica_imediata,
      numero_mesorregiao_geografica,
      nome_mesorregiao_geografica,
      numero_microrregiao_geografica,
      nome_microrregiao_geografica,
      codigo_municipio,
      nome_municipio,
      nome_regiao_nacional
) VALUES (
      {numero_uf_ibge}, '{nome_uf}', '{sigla_uf}', {numero_regiao_geografica_intermediaria}, 
      '{nome_regiao_geografica_intermediaria}', {numero_regiao_geografica_imediata}, 
      '{nome_regiao_geografica_imediata}', {numero_mesorregiao_geografica}, 
      '{nome_mesorregiao_geografica}', {numero_microrregiao_geografica}, 
      '{nome_microrregiao_geografica}', {codigo_municipio}, '{nome_municipio}', 
      '{nome_regiao_nacional}'
);

