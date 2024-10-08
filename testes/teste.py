from intelligentedb.schema.insertdimensions import insert_indicators_and_datapoints
from intelligentedb.schema.datastructures import  Indicator, DataPoint, DataPointIndicatorMap
from intelligentedb.schema.tablecreation import create_datapoints_dimension,create_indicators_dimension,create_junction_table,create_user_dtypes,create_city_dimension
from intelligentedb import DBconnection
from intelligentedb.schema.base_schema_files import fill_junction_table_base_vals, fill_dimension_tables_base_vals
from intelligentedb.etl import insert_df_into_fact_table
import pandas as pd


def test_dimension_and_junction_tables()->None:
   indicators = [
      Indicator(
         dimensao="Economia",
         topico="PIB",
         nome_indicador="indicador_teste1",
         instituicao_fonte_dados="IBGE"
      ),
      Indicator(
         dimensao="Demografia",
         topico="População",
         nome_indicador="indicador_teste2",
         instituicao_fonte_dados="IBGE"
      ),
      Indicator(
         dimensao="Saúde",
         topico="Expectativa de Vida",
         nome_indicador="indicador_teste3",
         instituicao_fonte_dados="Ministério da Saúde"
      )
   ]

   data_points = [
      DataPoint(
         nome_dado="dado_teste1",
         topico="Demografia",
         orgao_fonte="IBGE",
         forma_extracao="api",
         anos_serie_historica=[2000, 2010, 2020]
      ),
      DataPoint(
         nome_dado="dado_teste2",
         topico="Economia",
         orgao_fonte="IBGE",
         forma_extracao="ftp",
         anos_serie_historica=[2000, 2005, 2010]
      ),
      DataPoint(
         nome_dado="dado_teste3",
         topico="Saúde",
         orgao_fonte="Ministério da Saúde",
         forma_extracao="webscrapping",
         anos_serie_historica=[2000, 2015, 2020]
      )
   ]
      
   indicators_data_points_mapping = [
      DataPointIndicatorMap(data_point='dado_teste1', indicator='indicador_teste1'),
      DataPointIndicatorMap(data_point='dado_teste2', indicator='indicador_teste1'),
      DataPointIndicatorMap(data_point='dado_teste2', indicator='indicador_teste2'),
      DataPointIndicatorMap(data_point='dado_teste3', indicator='indicador_teste3'),
      DataPointIndicatorMap(data_point='dado_teste3', indicator='indicador_teste2'),
   ]

   insert_indicators_and_datapoints(
      indicators=indicators,
      data_points=data_points,
      indicators_data_points_relations=indicators_data_points_mapping
   )

   output = DBconnection.execute_query("""
   SELECT * FROM juncao_dados_indicador;
   """)
   print(output)
   
def recreate_tables():
  create_datapoints_dimension()
  create_indicators_dimension()
  create_city_dimension()
  create_junction_table()
  fill_dimension_tables_base_vals('dado')
  fill_dimension_tables_base_vals('indicador')
  fill_dimension_tables_base_vals('municipio')
  fill_junction_table_base_vals()

def drop_all_tables():
   """
   Não rodar isso em produção :)
   """
   list_tables_query = """
   SELECT table_name 
   FROM information_schema.tables 
   WHERE table_schema = 'public';
   """
   table_list = DBconnection.execute_query(list_tables_query)
   for table in table_list:
      table_name = table[0]
      drop_query = f"DROP TABLE IF EXISTS {table_name} CASCADE;"
      print(f"Dropping table: {table_name}")
      DBconnection.execute_query(drop_query,False)


def teste_qualquer_query(query:str):
   result = DBconnection.execute_query(query)
   print(result)
   pass

if __name__ == "__main__":
   #val = get_datapoint_dim_table_info('Pib percapita')
   #print(val)
   #df = pd.read_csv("IN016_AE - Índice de tratamento de esgoto.csv")
   #time_series_years:list[int] = list(df["ano"].value_counts().index)
   #insert_df_into_fact_table(df=df,data_name="IN016_AE - Índice de tratamento de esgoto",time_series_years=time_series_years)
   table_name: str = "fato_topico_agua_e_esgoto"
   query = f"""--sql
   SELECT 
    pg_size_pretty(pg_table_size('{table_name}')) AS table_size,
    pg_size_pretty(pg_indexes_size('{table_name}')) AS indexes_size,
    pg_size_pretty(pg_total_relation_size('{table_name}')) AS total_size;
   """

   query2 = f"""--sql
      SELECT
         column_name,
         data_type,
         is_nullable,
         column_default
      FROM
         information_schema.columns
      WHERE
         table_name = '{table_name}'
         AND table_schema = 'public';
   """

   
   teste_qualquer_query(query2)