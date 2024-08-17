from intelligentedb import DBconnection

__INDICATOR_TO_DATA_QUERY = """
SELECT 
   dimensao_dado.topico,
   dimensao_dado.dado_id,
   dimensao_dado.anos_serie_historica 
FROM dimensao_dado --começa a query da tabela de dimensões de dados. Seleciona essas 3 colunas
INNER JOIN juncao_dados_indicador on juncao_dados_indicador.dado_id = dimensao_dado.dado_id --inner join com tabela de juncao 
INNER JOIN dimensao_indicador ON dimensao_indicador.indicador_id = juncao_dados_indicador.indicador_id --inner join da tabela de juncao com tabela de indicadores
WHERE LOWER(REPLACE(dimensao_indicador.nome_indicador, ' ', '')) = LOWER(REPLACE('{nome_indicador}', ' ', '')); --filtra pela nome do indicador
"""

def base_query(indicator:str):
   result:list[tuple] = DBconnection.execute_query(__INDICATOR_TO_DATA_QUERY.format(nome_indicador = indicator))
   print(result)