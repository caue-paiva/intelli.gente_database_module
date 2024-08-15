import csv,os
from typing import Literal
import pandas as pd

def get_base_dimension_vals(dimension_name:Literal['dado','indicador','municipio'])->tuple[tuple,list[tuple]]:
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
