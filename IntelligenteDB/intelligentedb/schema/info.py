from intelligentedb import DBconnection

def get_table_names()->list[str]:
   results:list|None = None
   with DBconnection.get_cursor() as c:
      c.execute(
         """--sql 
         SELECT schemaname, tablename
         FROM pg_tables
         WHERE schemaname NOT IN ('pg_catalog', 'information_schema');
         """
      )
      results = c.fetchall()
   
   if results is None:
      raise RuntimeError("Falha ao executar a busca pelos nomes das tabelas")
   return list(map(lambda x: x[1],results)) #primeiro elemento da tupla é o nome do schema, o segundo é o nome da tabela

def table_exists(table_name:str)->bool:
   query = f"""--sql
         SELECT EXISTS (
         SELECT 1 
         FROM pg_tables
         WHERE tablename = '{table_name}'
         );
         """
   query_result = DBconnection.execute_query(query)
   return query_result[0][0]

def get_table_num_rows(table_name:str)->int:
   query = f"""--sql
            SELECT COUNT(*) FROM {table_name};
            """
   query_result = DBconnection.execute_query(query)
   return query_result[0][0]