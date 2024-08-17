SELECT 
   dimensao_dado.topico,
   dimensao_dado.dado_id,
   dimensao_dado.anos_serie_historica 
FROM dimensao_dado --começa a query da tabela de dimensões de dados. Seleciona essas 3 colunas
INNER JOIN juncao_dados_indicador on juncao_dados_indicador.dado_id = dimensao_dado.dado_id --inner join com tabela de juncao 
INNER JOIN dimensao_indicador ON dimensao_indicador.indicador_id = juncao_dados_indicador.indicador_id --inner join da tabela de juncao com tabela de indicadores
WHERE LOWER(REPLACE(dimensao_indicador.nome_indicador, ' ', '')) = LOWER(REPLACE('{nome_indicador}', ' ', '')); --filtra pela nome do indicador

UPDATE dimensao_dado
SET anos_serie_historica = ARRAY[{", ".join(map(str,new_time_series_years))}] --atualiza a série histórica
WHERE LOWER(REPLACE(nome_dado, ' ', '')) = LOWER(REPLACE('{data_name}', ' ', '')); --filtra pelo dado


SELECT municipio_id,codigo_municipio FROM dimensao_municipio;

SELECT topico,dado_id,anos_serie_historica FROM dimensao_dado
WHERE  LOWER(REPLACE(dimensao_dado.nome_dado, ' ', '')) = LOWER(REPLACE('{data_point_name}', ' ', ''));