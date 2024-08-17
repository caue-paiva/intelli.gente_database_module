CREATE TYPE TIPO_DADOS_EXTRAIDOS AS ENUM ('int','float','str','bool')
CREATE TABLE IF NOT EXISTS {table_or_topic_name} (
      fato_id SERIAL PRIMARY KEY, --pk para a tabela de fatos
      dado_id INT,
      CONSTRAINT fk_dado FOREIGN KEY (dado_id) REFERENCES dimensao_dado(dado_id), --fk para dimensão dos dados
      municipio_id INT,
      CONSTRAINT fk_municipio FOREIGN KEY (municipio_id) REFERENCES dimensao_municipio(municipio_id), --fk pra dimensão município
      ano INT NOT NULL CONSTRAINT numero_eh_ano CHECK (ano BETWEEN 1980 AND EXTRACT(YEAR FROM CURRENT_DATE)), --valor do ano deve estar entre 1980 e ano atual
      tipo_dado TIPO_DADOS_EXTRAIDOS NOT NULL, --enum pro tipo dos dado extraídos
      valor VARCHAR(20) NOT NULL -- valor será guardado como string e extraído conforme o tipo acima
   );