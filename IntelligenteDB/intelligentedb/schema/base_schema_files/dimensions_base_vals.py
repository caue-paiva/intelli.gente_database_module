import csv,os
from typing import Literal
from intelligentedb.schema.datastructures import DataPointIndicatorMap
from intelligentedb.schema.tablecreation import create_fact_table
from intelligentedb.utils import normalize_text
from intelligentedb import DBconnection

def __get_base_dimension_vals(dimension_name:Literal['dado','indicador','municipio'])->tuple[tuple,list[tuple]]:
   """
   Le o arquivo CSV base da tabela de dimensao de dados e retorna uma tupla com as colunas e 
   os valores do CSV.

   Return:
      (tuple[tuple,list[tuple]]): tupla cujo prim. elemento é uma tupla das colunas do CSV
      e o segundo elemento é uma lista de tuplas dos valores
   """
   file_name:str
   match(dimension_name):
      case 'dado':
         file_name = "dimensao_dado.csv"
      case 'indicador':
         file_name = 'dimensao_indicador.csv'
      case 'municipio':
         file_name = 'dimensao_municipio.csv'
      case _:
         raise RuntimeError("falha ao achar o nome do arquivo do schema dimensão")
   
   column_row = True
   columns:tuple[str,...]
   data_list:list[tuple] = []

   file_path:str = os.path.join(os.path.dirname(__file__),f"{file_name}")
   with open(file_path, mode='r', newline='') as file:
      csv_reader = csv.reader(file)
      for row in csv_reader:
         if column_row:
            columns = tuple(row)
            column_row = False
         else:
            data_list.append(tuple(row))
   
   return (columns,data_list)

def fill_dimension_tables_base_vals(dimension_name: Literal['dado', 'indicador', 'municipio']):
   city_dimension_vals:tuple[tuple,list] = __get_base_dimension_vals(dimension_name)
   result = DBconnection.insert_many_values(
      f"dimensao_{dimension_name}",
      city_dimension_vals[0],
      city_dimension_vals[1]
   )
   print(f"Tabela da dimensao {dimension_name} foi preenchida com os valores padrões")
   
   if dimension_name == 'dado':
      print("criando tabelas de fatos para os tópicos")
      topics:set[str] = set(map(lambda x: x[1],city_dimension_vals[1])) 
      print(topics)
      for topic in topics:
         create_fact_table(topic)

def __read_junction_table_csv()->list[DataPointIndicatorMap]:
   """
   Retorna uma lista de tuplas, cujo primeiro elemento é o dado e o segundo é o indicador
   """
   data_list:list[DataPointIndicatorMap] = []
   file_path:str = os.path.join(os.path.dirname(__file__),"juncao_dados_indicador.csv")
   with open(file_path, mode='r', newline='') as file:
      csv_reader = csv.reader(file)
      next(csv_reader) #pula a coluna de headers
      
      for row in csv_reader:
         data_point = row[0]
         indicator = row[1]
         if not data_point or not indicator:
            continue   
         data_list.append(DataPointIndicatorMap(
               data_point=normalize_text(data_point),
               indicator=normalize_text(indicator)
            )
         )
   
   return data_list

def fill_junction_table_base_vals()->None:
   """
   Adiciona os valores básicos (cerca de 36 dados para Cerca de 30 indicadores) na tabela de junção. Caso um valor no CSV de referência não esteja 
   nas tabelas de indicador ou de dados não adiciona na tabela de junção. 
   """
   data_maps:list[DataPointIndicatorMap] = __read_junction_table_csv()

   indicator_result = DBconnection.execute_query("""
      SELECT nome_indicador,indicador_id FROM dimensao_indicador;
   """,True)

   indicator_result = list(map(lambda x: (normalize_text(x[0]),x[1]),indicator_result))
   indicator_dict:dict = {indicator_name:pk for indicator_name,pk in indicator_result}

   data_result = DBconnection.execute_query("""
      SELECT nome_dado,dado_id FROM dimensao_dado;
   """,True)

   data_result = list(map(lambda x: (normalize_text(x[0]),x[1]),data_result))
   data_dict:dict = {data_name:pk for data_name,pk in data_result}

   data_maps:list[DataPointIndicatorMap] = [ 
            DataPointIndicatorMap( 
               data_point=data_map.data_point,
               indicator=data_map.indicator,
               data_point_pk=data_dict.get(data_map.data_point,-1),
               indicator_pk=indicator_dict.get(data_map.indicator,-1)
            ) 
            for  data_map in  data_maps                          
   ]

   data_maps = list(filter(lambda x: x.data_point_pk != -1 and x.indicator_pk != -1 ,data_maps))
   DBconnection.insert_many_values(
      "juncao_dados_indicador",
      ("dado_id","indicador_id"),
      [(data_point.data_point_pk,data_point.indicator_pk) for  data_point in data_maps]
   )
   print("Tabela de junção entre indicadores e dados foi preenchida com os valores padrões ")