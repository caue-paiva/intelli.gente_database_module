CREATE TYPE FORMA_EXTRACAO AS ENUM ("API","WEBSCRAPPING","FTP");

CREATE TABLE IF NOT EXISTS dimensao_dados (
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
   
   numero_uf_ibge INTEGER NOT NULL, --número da UF segundo o IBGE
   nome_uf VARCHAR(50) NOT NULL, --nome e sigla da UF
   sigla_uf VARCHAR(2) NOT NULL,

   numero_regiao_geografica_intermediaria INTEGER, --numero de divisões geográficas segundo o IBGE
   nome_regiao_geografica_intermediaria VARCHAR(100),
   
   numero_regiao_geografica_imediata INTEGER,
   nome_regiao_geografica_imediata VARCHAR(100),
   
   numero_mesorregiao_geografica INTEGER,
   nome_mesorregiao_geografica VARCHAR(100),
   
   numero_microrregiao_geografica INTEGER,
   nome_microrregiao_geografica VARCHAR(100),

   codigo_municipio INTEGER NOT NULL CONSTRAINT codigo_munic_7_digitos CHECK (codigo_municipio BETWEEN 1000000 AND 9999999), --código do município do IBGE, um inteiro de 7 dígitos
   nome_municipio VARCHAR(100) NOT NULL,

   nome_regiao_nacional VARCHAR(50) NOT NULL, --uma das 5 regiões do brasil
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
  instituicao_fonte_dados VARCHAR(100),
);