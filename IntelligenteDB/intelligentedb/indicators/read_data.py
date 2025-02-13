from intelligentedb import DBconnection
from intelligentedb.utils import parse_topic_table_name, to_postgres_list
from intelligentedb.query_fact_tables import get_datapoint_dim_table_info
import pandas as pd


def get_datapoints_values(datapoint_name:str,years:list[int] = [])->pd.DataFrame | None:
   """
   Retorna os valores de um dado armazenado numa tabela de fato,
   com a possibilidade de filtrar pelos anos dos dados

   Args:
      datapoint_name (str): O nome do ponto de dado a ser recuperado.
      years (list[int], optional): Lista de anos para filtrar os dados. Se não fornecido, retorna todos os anos.
   
   Returns:
         pd.DataFrame | None: Um DataFrame contendo os valores do dados e os anos correspondentes,
                        ou None se os dados não forem encontrados.
   """
   dimension_table_info:dict | None = get_datapoint_dim_table_info(datapoint_name) #pega nome do tópico do dado
   if dimension_table_info is None:
      return None

   fact_table_name:str = parse_topic_table_name(dimension_table_info["topico"]) #acha o nome da tabela fato a partir do tópico
   
   if years: #tem que filtrar por certos anos
      pg_years_list:str = to_postgres_list(years)
      
      query = F"""-- beginsql
      SELECT ano,tipo_dado,valor,municipio_id FROM {fact_table_name}
      WHERE ano in {pg_years_list};
      -- endsql
      """
   else:
      query = f"""-- beginsql
      SELECT ano,tipo_dado,valor,municipio_id FROM {fact_table_name};
      -- endsql
      """

   query_result = DBconnection.execute_query(query)

   if query_result:
      dtype = query_result[0][1] #pega o tipo de dado do dado
      data_dict = {"valor":[],"ano":[],"municipio_id":[]}

      for line in query_result:
         data_dict["ano"].append(line[0])
         data_dict["valor"].append(line[2])
         data_dict["municipio_id"].append(line[3])
      
      df = pd.DataFrame(data_dict)
      df["valor"] = df["valor"].astype(dtype)

      return df
   else:
      return None

def get_city_dimension_values()->pd.DataFrame:
   cols = [
    "municipio_id",
    "numero_uf_ibge",
    "nome_uf",
    "sigla_uf",
    "numero_regiao_geografica_intermediaria",
    "nome_regiao_geografica_intermediaria",
    "numero_regiao_geografica_imediata",
    "nome_regiao_geografica_imediata",
    "numero_mesorregiao_geografica",
    "nome_mesorregiao_geografica",
    "numero_microrregiao_geografica",
    "nome_microrregiao_geografica",
    "codigo_municipio",
    "nome_municipio",
    "nome_regiao_nacional"
   ]


   query = """--- beginsql
   SELECT * FROM dimensao_municipio;
   -- endsql
   """

   result = DBconnection.execute_query(query)

   df = pd.DataFrame(result,columns=cols)
   return df