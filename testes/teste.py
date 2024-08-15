from intelligentedb.schema.insertdimensions import insert_indicators_and_datapoints
from intelligentedb.schema.datastructures import  Indicator, DataPoint, DataPointIndicatorMap
from intelligentedb.schema.tablecreation import create_datapoints_dimension,create_indicators_dimension,create_junction_table,create_user_dtypes
from intelligentedb import DBconnection
from intelligentedb.schema.base_schema_files import get_base_dimension_vals

def test_dimension_and_junction_tables()->None:
   indicators = [
      Indicator(
         dimensao="Economia",
         topico="PIB",
         nome_indicador="Crescimento do PIB",
         instituicao_fonte_dados="IBGE"
      ),
      Indicator(
         dimensao="Demografia",
         topico="População",
         nome_indicador="Censo Populacional",
         instituicao_fonte_dados="IBGE"
      ),
      Indicator(
         dimensao="Saúde",
         topico="Expectativa de Vida",
         nome_indicador="Expectativa de Vida ao Nascer",
         instituicao_fonte_dados="Ministério da Saúde"
      )
   ]

   data_points = [
      DataPoint(
         nome_dado="Censo Populacional",
         topico="Demografia",
         orgao_fonte="IBGE",
         forma_extracao="api",
         anos_serie_historica=[2000, 2010, 2020]
      ),
      DataPoint(
         nome_dado="PIB Anual",
         topico="Economia",
         orgao_fonte="IBGE",
         forma_extracao="ftp",
         anos_serie_historica=[2000, 2005, 2010]
      ),
      DataPoint(
         nome_dado="Expectativa de Vida",
         topico="Saúde",
         orgao_fonte="Ministério da Saúde",
         forma_extracao="webscrapping",
         anos_serie_historica=[2000, 2015, 2020]
      )
   ]
      
   indicators_data_points_mapping = [
      DataPointIndicatorMap(data_point='PIB Anual', indicator='Crescimento do PIB'),
      DataPointIndicatorMap(data_point='Censo Populacional', indicator='Crescimento do PIB'),
      DataPointIndicatorMap(data_point='Censo Populacional', indicator='Censo Populacional'),
      DataPointIndicatorMap(data_point='Expectativa de Vida', indicator='Expectativa de Vida ao Nascer'),
      DataPointIndicatorMap(data_point='Expectativa de Vida', indicator='Censo Populacional'),
   ]

   #create_user_dtypes()
   create_datapoints_dimension()
   create_indicators_dimension()
   create_junction_table()

   insert_indicators_and_datapoints(
      indicators=indicators,
      data_points=data_points,
      indicators_data_points_relations=indicators_data_points_mapping
   )

   output = DBconnection.execute_query("""
   SELECT * FROM juncao_dados_indicador;
   """)
   print(output)


if __name__ == "__main__":
   city_dimension_vals:tuple[tuple,list] = get_base_dimension_vals('indicador')

   result = DBconnection.insert_many_values(
      "teste_indicador2",
      city_dimension_vals[0],
      city_dimension_vals[1]
   )