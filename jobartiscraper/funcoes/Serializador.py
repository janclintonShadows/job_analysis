
def serialize_data(valor)->int:
    """
    Pega uma valor de uma data em forma de texto, converta para datetime.date, e compara a data com a data atual, se a data for maior que a data atual retorna o ano - 1, caso contrario retorna o ano.

    Args: 
        value (str): O valor da data a ser formatado.
    
    Returns: 
        int: correspondente ao ano que o recrutamento foi iniciado.
    """
    from datetime import datetime as dt


    data = dt.strptime(valor,'%d/%m/%Y')
    data_hoje = dt.today()

    if data > data_hoje:
        return data.year - (data.year - data_hoje.year)
    else:
        return data.year

def serialize_split_num_part(valor)->int:
    """
    Pega uma valor de texto, separa e pega apenas a parte inteira do valor.

    Args: 
        value (str): O valor texto contendo um numero.
    
    Returns: 
        int: correspondente ao ano que o recrutamento foi iniciado.
    """
    import re
    # compilando a expressão que vai pegar os numeros
    try:
        r = valor.split(' ')
        return int(r[0])
    except Exception as e:
        print(f'Ocorreu um erro {e}')