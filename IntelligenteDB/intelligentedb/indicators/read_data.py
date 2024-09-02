from intelligentedb import DBconnection
from intelligentedb.utils import parse_topic_table_name
from intelligentedb.query_fact_tables import get_datapoint_dim_table_info
import pandas as pd


def get_datapoints(datapoint_name:str,years:list[int] = [])->pd.DataFrame:
   dimension_table_info:dict = get_datapoint_dim_table_info(datapoint_name)
   fact_table_name:str = parse_topic_table_name(dimension_table_info["topico"])
   time_series_years:list[int] = dimension_table_info["anos_serie_historica"]
   

