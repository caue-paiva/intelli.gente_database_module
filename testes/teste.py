from intelligentedb.schema.insertdimensions import insert_indicators_and_datapoints
from intelligentedb.schema.datastructures import  Indicator, DataPoint, DataPointIndicatorMap
from intelligentedb.schema.tablecreation import create_datapoints_dimension,create_indicators_dimension,create_junction_table,create_user_dtypes,create_city_dimension
from intelligentedb import DBconnection
from intelligentedb.schema.base_schema_files import fill_junction_table_base_vals, fill_dimension_tables_base_vals
from intelligentedb.etl import base_query

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

def etl_test():
   pass


if __name__ == "__main__":
   recreate_tables()
   test_dimension_and_junction_tables()
