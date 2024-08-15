from intelligentedb import DBconnection,DEFAULT_VAL_INT_COLS,DEFAULT_VAL_STR_COLS
import psycopg2
from typing import Literal

def insert_new_city(
    codigo_municipio: int,
    nome_municipio: str,
    nome_uf: str,
    sigla_uf: str,
    nome_regiao_nacional: str,
    numero_uf_ibge: int = -1,
    numero_regiao_geografica_intermediaria: int = -1,
    nome_regiao_geografica_intermediaria: str = 'n/a',
    numero_regiao_geografica_imediata: int = -1,
    nome_regiao_geografica_imediata: str = 'n/a',
    numero_mesorregiao_geografica: int = -1,
    nome_mesorregiao_geografica: str = 'n/a',
    numero_microrregiao_geografica: int = -1,
    nome_microrregiao_geografica: str = 'n/a'
) -> None:
   """
   Tenta inserir uma cidade à tabela de dimensão de município, gera um erro se falhar.
   """
   query = f'''--sql
            INSERT INTO dimensao_municipio (
                numero_uf_ibge,
                nome_uf,
                sigla_uf,
                numero_regiao_geografica_intermediaria,
                nome_regiao_geografica_intermediaria,
                numero_regiao_geografica_imediata,
                nome_regiao_geografica_imediata,
                numero_mesorregiao_geografica,
                nome_mesorregiao_geografica,
                numero_microrregiao_geografica,
                nome_microrregiao_geografica,
                codigo_municipio,
                nome_municipio,
                nome_regiao_nacional
            ) VALUES (
                 {numero_uf_ibge}, '{nome_uf}', '{sigla_uf}', {numero_regiao_geografica_intermediaria}, 
                '{nome_regiao_geografica_intermediaria}', {numero_regiao_geografica_imediata}, 
                '{nome_regiao_geografica_imediata}', {numero_mesorregiao_geografica}, 
                '{nome_mesorregiao_geografica}', {numero_microrregiao_geografica}, 
                '{nome_microrregiao_geografica}', {codigo_municipio}, '{nome_municipio}', 
                '{nome_regiao_nacional}'
            );
   '''
   DBconnection.execute_query(query)

def insert_new_indicator(
    dimensao: str,
    topico: str,
    nome_indicador: str,
    instituicao_fonte_dados: str,
    nivel_indicador: int = DEFAULT_VAL_INT_COLS,
    subdimensao: str = DEFAULT_VAL_STR_COLS,
    tipo: Literal['principal', 'adicional', 'n/a'] = DEFAULT_VAL_STR_COLS,
    relevancia: Literal["média", "baixa", "alta", "n/a"] = DEFAULT_VAL_STR_COLS,
    peso_estatistico: int = DEFAULT_VAL_INT_COLS,
    texto_explicativo_indicador: str = DEFAULT_VAL_STR_COLS
) -> int:
   """
   Tenta inserir um novo indicador na tabela de dimensão de indicadores

   Return:
      (int): Primary key do novo indicador
   """
   query = f'''--sql
            INSERT INTO dimensao_indicador (
                dimensao,
                subdimensao,
                topico,
                nome_indicador,
                nivel_indicador,
                tipo,
                relevancia,
                peso_estatistico,
                texto_explicativo_indicador,
                instituicao_fonte_dados
            ) VALUES (
                '{dimensao}', '{subdimensao}', '{topico}', '{nome_indicador}', 
                {nivel_indicador}, '{tipo}', '{relevancia}', 
                {peso_estatistico}, '{texto_explicativo_indicador}', '{instituicao_fonte_dados}'
            ) RETURNING indicador_id;
   '''
   result:list[tuple] = DBconnection.execute_query(query)
   return result[0][0]

def insert_new_datapoint(
      nome_dado:str,
      topico:str,
      orgao_fonte:str,
      forma_extracao: Literal['api','webscrapping','ftp','n/a'],
      anos_serie_historica:list[int]
)->int:
   """
   Tenta inserir um novo dado na tabela de dimensão de dados

   Return:
      (int): Primary key do novo dado
   """
   query = f'''--sql
            INSERT INTO dimensao_dado (
                nome_dado,
                topico,
                orgao_fonte,
                forma_extracao,
                anos_serie_historica
            ) VALUES (
                '{nome_dado}', '{topico}', '{orgao_fonte}', '{forma_extracao}', '{{{", ".join(map(str, anos_serie_historica))}}}'
            ) RETURNING dado_id;
   '''
   result:list[tuple] = DBconnection.execute_query(query)
   return result[0][0]


def insert_junction_table_vals(
    ids_dado_e_indicador:list[tuple[int,int]]
)->None:
   """
   Insere valores na tabela de junção entre indicadores e dados.Gera erro caso a query falhe

   Args:
      ids_dado_e_indicador (list[tuple[int]]: lista de tuplas cujo primeiro elemento é o id (pk) do dado e o segundo é o id (pk) do indicador
   Return:
      (None)
   """
   values_str = ",".join(f"({dado_id}, {indicador_id})" for dado_id, indicador_id in ids_dado_e_indicador)

   query = f"""
   INSERT INTO juncao_dados_indicador(dado_id,indicador_id) VALUES 
        {values_str};
   """
   DBconnection.execute_query(query)