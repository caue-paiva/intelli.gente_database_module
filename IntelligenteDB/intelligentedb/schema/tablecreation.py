from intelligentedb import DBconnection

def create_user_dtypes()->None:
   """
   Cria tipos de dados definidos pelo usuário, necessário para executar as outras funções
   """
   query = """
      CREATE TYPE TIPO_INDICADOR AS ENUM ('principal','adicional','n/a');
      CREATE TYPE RELEVANCIA_INDICADOR AS ENUM ('alta','media','baixa','n/a');
      CREATE TYPE TIPO_DADOS_EXTRAIDOS AS ENUM ('int','float','str','bool');
      CREATE TYPE FORMA_EXTRACAO AS ENUM ('api','webscrapping','ftp');
   """
   DBconnection.execute_query(query,return_data=False)

def create_city_dimension()->None:
   """
   Tenta criar tabela de dimensão do município,gera erro se não conseguir
   """
   query = """--sql
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

      nome_regiao_nacional VARCHAR(50) NOT NULL --uma das 5 regiões do brasil
   );
   """
   DBconnection.execute_query(query,return_data=False)

def create_datapoints_dimension()->None:
   """
   Tenta criar tabela de dimensão dos dados,gera erro se não conseguir
   """
   query = """--sql
   CREATE TABLE IF NOT EXISTS dimensao_dado (
      dado_id SERIAL PRIMARY KEY,
      nome_dado VARCHAR(100) NOT NULL,
      topico VARCHAR(50) NOT NULL, --topico do dado, é tambem o nome da tabela que vamos utilizar para carregar os dados
      orgao_fonte VARCHAR(50), -- orgão do governo 
      forma_extracao FORMA_EXTRACAO, --enum para forma de extração dos dados
      anos_serie_historica INTEGER ARRAY --lista de anos de série histórica que os dados tem
   );
   """
   DBconnection.execute_query(query,return_data=False)

def create_indicators_dimension()->None:
   """
   Tenta criar tabela de dimensão dos indicadores ,gera erro se não conseguir
   """
   query = """--sql
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
      instituicao_fonte_dados VARCHAR(100)
   );
   """
   DBconnection.execute_query(query,return_data=False)

def create_junction_table()->None:
   """
   Tenta criar tabela de junção entre a dimensão dos indicadores e dos dados, gera erro se não conseguir
   """
   query = """--sql
   CREATE TABLE IF NOT EXISTS juncao_dados_indicador (
      dado_id INT,
      indicador_id INT,
      CONSTRAINT fk_dado FOREIGN KEY (dado_id) REFERENCES dimensao_dado(dado_id),
      CONSTRAINT fk_indicador FOREIGN KEY (indicador_id) REFERENCES dimensao_indicador(indicador_id),
      PRIMARY KEY (dado_id, indicador_id) --guarante que a combinação desses dados é única, ou seja não podem existir linhas duplicadas 
   );
   """
   DBconnection.execute_query(query,return_data=False)

def create_fact_table(table_or_topic_name:str)->None:
   query = f"""--sql
   CREATE TABLE IF NOT EXISTS {table_or_topic_name} (
      fato_id SERIAL PRIMARY KEY, --pk para a tabela de fatos
      dado_id INT,
      CONSTRAINT fk_dado FOREIGN KEY (dado_id) REFERENCES dimensao_dado(dado_id), --fk para dimensão dos dados
      municipio_id INT
      CONSTRAINT fk_municipio FOREIGN KEY (municipio_id) REFERENCES dimensao_municipio(municipio_id), --fk pra dimensão município
      ano INT NOT NULL CONSTRAINT numero_eh_ano CHECK (numero_eh_ano BETWEEN 1980 AND EXTRACT(YEAR FROM CURRENT_DATE)) --valor do ano deve estar entre 1980 e ano atual
      tipo_dado TIPO_DADOS_EXTRAIDOS NOT NULL, --enum pro tipo dos dado extraídos
      valor VARCHAR(50) NOT NULL -- valor será guardado como string e extraído conforme o tipo acima
   );
   """
   DBconnection.execute_query(query,return_data=False)