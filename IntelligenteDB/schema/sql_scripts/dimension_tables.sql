CREATE TYPE FORMA_EXTRACAO AS ENUM ("API","WEBSCRAPPING","FTP");

CREATE TABLE dimensao_dados (
  dado_id SERIAL PRIMARY KEY,
  nome_dado VARCHAR(100) NOT NULL,
  topico VARCHAR(50) NOT NULL, --topico do dado, é tambem o nome da tabela que vamos utilizar para carregar os dados
  orgao_fonte VARCHAR(50), -- orgão do governo 
  forma_extracao FORMA_EXTRACAO, --enum para forma de extração dos dados
  fonte_extracao VARCHAR (250), -- fonte dos dados, ou nome da api ou link
  anos_serie_historica INTEGER ARRAY --lista de anos de série histórica que os dados tem
);


CREATE TABLE dimensao_municipio (
   municipio_id SERIAL PRIMARY KEY,
   
   codigo_uf_ibge INTEGER NOT NULL, --codigo da UF segundo o IBGE
   nome_uf VARCHAR(50) NOT NULL, --nome e sigla da UF
   sigla_uf VARCHAR(2) NOT NULL,

   nome_regiao_nacional VARCHAR(50) NOT NULL, --uma das 5 regiões do brasil
   codigo_regiao_nacional INTEGER NOT NULL,

   
   codigo_regiao_geografica_intermediaria INTEGER,
   nome_regiao_geografica_intermediaria VARCHAR(100),
   
   codigo_regiao_geografica_imediata INTEGER,
   nome_regiao_geografica_imediata VARCHAR(100),
   
   codigo_mesorregiao_geografica INTEGER,
   nome_mesorregiao_geografica VARCHAR(100),
   
   codigo_microrregiao_geografica INTEGER,
   nome_microrregiao_geografica VARCHAR(100),






);