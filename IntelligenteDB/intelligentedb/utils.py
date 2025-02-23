import unicodedata, string, re

def remove_non_en_chars(input_str:str)->str:
    normalized_text = unicodedata.normalize('NFKD', input_str)
    return normalized_text.encode('ascii', 'ignore').decode('ascii')

def normalize_text(input_str:str)->str:
   """
   dado um input, remove espaços, \n,\r, \t, chars não ASCII, whitespace e faz tudo ser lowercase 
   """
   str_:str = remove_non_en_chars(input_str)
   str_ =  "".join(filter(lambda x: x in string.printable, str_))
   return str_.replace(" ","").lower()

def parse_topic_table_name(data_topic:str,indicator_table = False)->str:
    """
    Transforma o nome de um tópico de um indicador em um nome de tabela aceitado pelo PG SQL e padronizado, começando com fato_topico_
    """
    str_:str = remove_non_en_chars(data_topic)
   
    str_ = str_.replace(" ", "_").replace("-", "_")
    str_ = str_.lower()
    str_ = str_.strip()
    
    # remove todos chars que não são letras, underscore ou números
    str_ = re.sub(r'[^a-zA-Z0-9_]', '', str_)
    
    #truncar para o tamanho max de um identificador do postgres

    if indicator_table:
        return f"indicador_fato_topico_{str_[:52]}"
    else:
        return f"fato_topico_{str_[:63]}"

def to_postgres_list(py_list:list)->str:
    """
    Converte uma lista Python em uma string de lista do PostgreSQL.
    
    Args:
        py_list (list): A lista Python a ser convertida.
    
    Return:
        str: Uma string formatada como uma lista do PostgreSQL.
    """
    if not py_list:
        return "()"
    
    def format_item(item):
        #se o item for uma sstring, coloca ele em aspas duplas
        if isinstance(item, str):
            escaped = item.replace("'", "''")
            return f"'{escaped}'"
        
        #senao apenas converte para str
        return str(item)
    
    formatted_items = ",".join(format_item(item) for item in py_list)
    return f"({formatted_items})"
    