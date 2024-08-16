from intelligentedb import DEFAULT_VAL_INT_COLS,DEFAULT_VAL_STR_COLS
from typing import Literal
from dataclasses import dataclass, field

@dataclass
class Indicator:
    dimensao: str
    topico: str
    nome_indicador: str
    instituicao_fonte_dados: str
    nivel_indicador: int = DEFAULT_VAL_INT_COLS
    subdimensao: str = DEFAULT_VAL_STR_COLS
    tipo: Literal['principal', 'adicional', 'n/a'] = DEFAULT_VAL_STR_COLS
    relevancia: Literal["média", "baixa", "alta", "n/a"] = DEFAULT_VAL_STR_COLS
    peso_estatistico: int = DEFAULT_VAL_INT_COLS
    texto_explicativo_indicador: str = DEFAULT_VAL_STR_COLS

@dataclass
class DataPoint:
    nome_dado: str
    topico: str
    orgao_fonte: str
    anos_serie_historica: list[int] = field(default_factory=list)
    forma_extracao: Literal['api', 'webscrapping', 'ftp', 'n/a'] = DEFAULT_VAL_STR_COLS

@dataclass
class DataPointIndicatorMap:
   data_point:str
   indicator:str
   data_point_pk:int = -1
   indicator_pk:int = -1