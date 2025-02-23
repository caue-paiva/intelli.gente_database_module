from intelligentedb import DBconnection
from intelligentedb.utils import parse_topic_table_name,replace_city_codes_with_pk
from intelligentedb.query_fact_tables import get_indicador_dim_table_info
import pandas as pd

INDICATOR_SCORE_NULL_VAL = -1 #valor a ser inserido no lugar da nota do indicador quando o valor for nulo




def insert_df_indicators_table(df:pd.DataFrame,has_indicator_score = False)->None:
   """
   Insere os dados de um indicador (no formato de DF) na tabela de fatos (indicador_fato) correspondente

   Args:
      df (pd.DataFrame): Dados do indicador. Tem que ter as colunas: (ano,codigo_municipio,valor,indicador,tipo_dado)
         e de forma opcional uma coluna com a nota do indicador

      has_indicator_score (bool): diz se o df dos dados do indicador tem a nota do indicador 
   
   Return:
      (None)
   """

   if df.shape[0] < 1:
      raise RuntimeError("Dataframe passado como argumento deve ter mais de uma linha")
   
   indicator_name:str = df["indicador"].iloc[0]
   indicator_info :dict = get_indicador_dim_table_info(indicator_name)
   indicator_id:int = int(indicator_info["indicator_id"])
   topic:str = indicator_info["topico"]
   table_name:str = parse_topic_table_name(topic,indicator_table=True)

   df["codigo_municipio"] = replace_city_codes_with_pk(df["codigo_municipio"]) #troca código do município pela fk desse munic na tabela de dimensao
   fact_table_cols =  (
      'municipio_id',
      'indicador_id',
      'ano',
      'tipo_dado',
      'valor',
      'nivel_maturidade'
   )

   df_rows:list[tuple] = []
   for row in df.itertuples(index=False):
      ano = (row.ano)
      codigo_municipio = (row.codigo_municipio)
      valor = str(row.valor)
      tipo_dado = row.tipo_dado

      if has_indicator_score: #tem nota do indicador de 1 a 7 
         nota_indicador = (row.nota_indicador)
         df_rows.append(
            (codigo_municipio,indicator_id,ano,tipo_dado,valor,nota_indicador)
         )
      else:
         df_rows.append(
            (codigo_municipio,indicator_id,ano,tipo_dado,valor,INDICATOR_SCORE_NULL_VAL)
         )

   print(df_rows)
   DBconnection.insert_many_values(
      table_name=table_name,
      columns_tuple=fact_table_cols,
      values_list=df_rows,
      batch_size=2500
   )