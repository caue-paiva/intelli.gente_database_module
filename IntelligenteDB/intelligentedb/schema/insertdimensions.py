from intelligentedb import DBconnection
from intelligentedb.schema.datastructures import Indicator,DataPoint,DataPointIndicatorMap



def insert_new_city(
    codigo_municipio: int,
    nome_municipio: str,
    nome_uf: str,
    sigla_uf: str,
    nome_regiao_nacional: str,
    numero_uf_ibge: int = -1,
    numero_regiao_geografica_intermediaria: int = -1,
    nome_regiao_geografica_intermediaria: str = 'n/a',
    numero_regiao_geografica_imediata: int = -1,
    nome_regiao_geografica_imediata: str = 'n/a',
    numero_mesorregiao_geografica: int = -1,
    nome_mesorregiao_geografica: str = 'n/a',
    numero_microrregiao_geografica: int = -1,
    nome_microrregiao_geografica: str = 'n/a'
) -> None:
   """
   Tenta inserir uma cidade à tabela de dimensão de município, gera um erro se falhar.
   """
   query = f'''--sql
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
   '''
   DBconnection.execute_query(query)

def __insert_new_indicators(
    indicators:list[Indicator]
) -> dict[str,int]:
   """
   Tenta inserir vários novos indicador na tabela de dimensão de indicadores

   Return:
      (dict[str,int]): dict cujas keys são o nome de cada dado e seu valor é a pk que foi atribuida a ele
   """
   values = ", ".join(
        f"('{ind.dimensao}', '{ind.subdimensao}', '{ind.topico}', '{ind.nome_indicador}', "
        f"{ind.nivel_indicador}, '{ind.tipo}', '{ind.relevancia}', {ind.peso_estatistico}, "
        f"'{ind.texto_explicativo_indicador}', '{ind.instituicao_fonte_dados}')"
        for ind in indicators
    )
   query = f'''--sql
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
   '''
  
   result:list[tuple] = DBconnection.execute_query(query)
   indicator_name_and_pk:dict[str,int] = {} #dict cuja key é o nome do indicador e seu valor é a pk que foi atribuida a ele
   
   for insertion_result,indicator in  zip(result,indicators):
      indicator_name_and_pk[indicator.nome_indicador] = insertion_result[0] 
   return indicator_name_and_pk

def __insert_new_datapoints(
      data_points:list[DataPoint]
)->dict[str,int]:
   """
   Tenta inserir novos dado na tabela de dimensão de dados

   Return:
      (int): Primary key do novo dado
   """
   values = ", ".join(
        f"('{dp.nome_dado}', '{dp.topico}', '{dp.orgao_fonte}', '{dp.forma_extracao}', '{{{', '.join(map(str, dp.anos_serie_historica))}}}')"
        for dp in data_points
   )  

   query = f'''--sql
            INSERT INTO dimensao_dado (
                nome_dado,
                topico,
                orgao_fonte,
                forma_extracao,
                anos_serie_historica
            ) VALUES 
               {values}
            RETURNING dado_id;
   '''
   result:list[tuple] = DBconnection.execute_query(query,return_data=True)
   data_name_and_pk:dict[str,int] = {} #dict cuja key é o nome do dado e seu valor é a pk que foi atribuida a ele
   
   for insertion_result,data_point in  zip(result,data_points):
      data_name_and_pk[data_point.nome_dado] = insertion_result[0] 
   return data_name_and_pk

def __insert_junction_table_vals(
    ids_dado_e_indicador:list[tuple[int,int]]
)->None:
   """
   Insere valores na tabela de junção entre indicadores e dados.Gera erro caso a query falhe

   Args:
      ids_dado_e_indicador (list[tuple[int]]: lista de tuplas cujo primeiro elemento é o id (pk) do dado e o segundo é o id (pk) do indicador
   Return:
      (None)
   """
   values_str = ",".join(f"({dado_id}, {indicador_id})" for dado_id, indicador_id in ids_dado_e_indicador)

   query = f"""
   INSERT INTO juncao_dados_indicador(dado_id,indicador_id) VALUES 
        {values_str};
   """
   DBconnection.execute_query(query,return_data=False)

def insert_indicators_and_datapoints(
    indicators:list[Indicator],
    data_points:list[DataPoint],
    indicators_data_points_relations:list[DataPointIndicatorMap]
)->None:
   """
   Args:
     indicators
     data_points
     indicators_data_points_relations (list[tuple[str,str]]): lista de tuplas cuja primeiro elemento é o nome do dado e o segundo é o nome do indicador 
   
   """
   data_points_pk:dict = __insert_new_datapoints(data_points) #dict com nome do dado e sua pk ex: {"Taxa de Analfabetismo": 1862}
   print(data_points_pk)
   indicators_pk = __insert_new_indicators(indicators) #dict com nome do indicador e sua pk ex: {"Cobertura de 5G": 9028}
   print(indicators_pk)
   
   map_relations_to_pk = lambda x: ( data_points_pk[x.data_point], indicators_pk[x.indicator] )
   list_relations_with_pk:list[tuple[int,int]] = list(map(map_relations_to_pk,indicators_data_points_relations))
   print(list_relations_with_pk) 

   __insert_junction_table_vals(list_relations_with_pk)