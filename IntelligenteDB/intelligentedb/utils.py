import unicodedata, string

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


    