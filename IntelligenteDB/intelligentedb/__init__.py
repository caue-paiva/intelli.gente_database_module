import os, psycopg2
from psycopg2.extensions import connection,cursor
from dotenv import load_dotenv
from contextlib import contextmanager 
from typing import Generator,Any
import atexit

load_dotenv(os.path.join(os.path.dirname(__file__), "db_connection.env"))

class DBconnection():
   __CONNECTION: connection | None = None #variável de classe para conexão com db

   @classmethod
   def get_connection(cls)-> connection:
      if cls.__CONNECTION is None:
         cls.__CONNECTION = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USERNAME"),
            password=os.getenv("DB_PASSWORD")
         )
         print("connection created")
      return cls.__CONNECTION
   
   @classmethod
   def close_connection(cls)->None:
      if cls.__CONNECTION is not None:
         cls.__CONNECTION.close()
         cls.__CONNECTION = None
    
   @classmethod
   @contextmanager
   def get_cursor(cls)->Generator[cursor,Any,Any]:
      """
      context manager para gerenciar cursores da conexão com BD
      Ex:

      with DBconnection.get_cursor() as c:
         c.execute(query)
      """
      if cls.__CONNECTION is None: #cria uma conexão caso seja necessário
         cls.__CONNECTION = cls.get_connection()
      cursor = cls.__CONNECTION.cursor()
      try:
            yield cursor  # Provide the cursor to the context
      finally:
            cursor.close()  # Ensure the cursor is closed

   @classmethod
   def execute_query(cls,query:str)->list[tuple]:
      query_result:list|None = None
      with cls.get_cursor() as c:
         c.execute(query)
         query_result = c.fetchall()
      if query_result is None:
         raise RuntimeError(f"Falha ao executar a Query: {query}")
      return query_result
   
atexit.register(DBconnection.close_connection) # type: ignore #fecha a conexão quando o programa parar de executar
from . import DBconnection