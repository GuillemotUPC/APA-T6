import re

# El teu diccionari global
PALABRAS_A_NUM = {
    'en punto': 0, 'una': 1, 'un': 1, 'dos': 2, 'tres': 3, 'cuatro': 4, 
    'cinco': 5, 'seis': 6, 'siete': 7, 'ocho': 8, 'nueve': 9, 'diez': 10, 
    'once': 11, 'doce': 12, 'trece': 13, 'catorce': 14, 'quince': 15,
    'dieciséis': 16, 'diez y seis': 16, 'diecisiete': 17, 'diez y siete': 17,
    'dieciocho': 18, 'diez y ocho': 18, 'diecinueve': 19, 'diez y nueve': 19,
    'veinte': 20, 'treinta': 30, 'cuarenta': 40, 'cincuenta': 50,
    'veintiuno': 21, 'veinte y uno': 21, 'veintidós': 22, 'veinte y dos': 22,
    'veintitres': 23, 'veintitrés': 23, 'veinte y tres': 23, 'veinticuatro': 24,
    'veinticinco': 25, 'veinte y cinco': 25, 'veintiséis': 26, 'veinte y seis': 26,
    'veintisiete': 27, 'veinte y siete': 27, 'veintiocho': 28, 'veinte y ocho': 28,
    'veintinueve': 29, 'veinte y nueve': 29,
    'treinta y uno': 31, 'treinta y dos': 32, 'treinta y tres': 33, 'treinta y cuatro': 34,
    'treinta y cinco': 35, 'treinta y seis': 36, 'treinta y siete': 37, 'treinta y ocho': 38,
    'treinta y nueve': 39,
    'cuarenta y uno': 41, 'cuarenta y dos': 42, 'cuarenta y tres': 43, 'cuarenta y cuatro': 44,
    'cuarenta y cinco': 45, 'cuarenta y seis': 46, 'cuarenta y siete': 47, 'cuarenta y ocho': 48,
    'cuarenta y nueve': 49,
    'cincuenta y uno': 51, 'cincuenta y dos': 52, 'cincuenta y tres': 53, 'cincuenta y cuatro': 54,
    'cincuenta y cinco': 55, 'cincuenta y seis': 56, 'cincuenta y siete': 57, 'cincuenta y ocho': 58,
    'cincuenta y nueve': 59
}

# Diccionari fet amb IA, com no era part de la tasca i per agilitzar tot l'he fet tot amb IA.

def normalizaHora(string):
    """
    Normaliza expresiones horarias en formato HH:MM de 24 horas.
    
    >>> normalizaHora('17:05')
    '17:05'
    >>> normalizaHora('8:27')
    '08:27'
    >>> normalizaHora('23h31m')
    '23h31m'
    >>> normalizaHora('las ocho y veintisiete')
    '08:27'
    >>> normalizaHora('las once en punto')
    '11:00'
    >>> normalizaHora('las 3 de la tarde')
    '15:00'
    >>> normalizaHora('las 8 de la mañana')
    '08:00'
    >>> normalizaHora('las 11 de la tarde') # Error: 11 de la tarde no existeix (seria noche)
    >>> normalizaHora('las 13 de la tarde') # Error: Excedeix format 12h
    """
    string = string.strip()

    # --- FORMAT 1: DIGITAL ---
    patron_digital = re.compile(r'^(\d{1,2})[:h](\d{2})m?$')
    match_digital = patron_digital.match(string)
    
    if match_digital:
        hora = match_digital.group(1)
        minutos = match_digital.group(2)
        if len(hora) == 1: hora = "0" + hora
        if int(hora) < 24 and int(minutos) < 60:
            return f"{hora}:{minutos}"
        return None

    # --- FORMAT 2: TEXT COMPLET ---
    patron_texto = re.compile(r'^las\s+(.+?)(?:\s+y\s+(.+?)|\s+(en\s+punto))$')
    match_texto = patron_texto.match(string)
    
    if match_texto:
        hora_txt = match_texto.group(1)      
        minutos_txt = match_texto.group(2)   
        en_punto_txt = match_texto.group(3)  
        
        if hora_txt in PALABRAS_A_NUM:
            hora_num = PALABRAS_A_NUM[hora_txt]
        else: return None 
            
        if en_punto_txt == 'en punto':
            minutos_num = 0
        elif minutos_txt in PALABRAS_A_NUM:
            minutos_num = PALABRAS_A_NUM[minutos_txt]
        else: return None 
            
        hora_final = str(hora_num)
        minutos_final = str(minutos_num)
        if len(hora_final) == 1: hora_final = "0" + hora_final
        if len(minutos_final) == 1: minutos_final = "0" + minutos_final
            
        return f"{hora_final}:{minutos_final}"

    # FORMAT 3: TEXT AMB  ("las 3 de la tarde") ---
    patron_franja = re.compile(r'^las\s+(\d{1,2})\s+de\s+la\s+(mañana|tarde)$')
    match_franja = patron_franja.match(string)
    
    if match_franja:
        hora_num = int(match_franja.group(1))
        franja = match_franja.group(2)
        
        # Validació: En format 12h, el número no pot ser superior a 12
        if hora_num > 12 or hora_num < 1:
            return None
            
        # Lògica de la franja
        if franja == 'tarde':
            # 'tarde' accepta des de les 1 (13:00) fins a les 8 o 9 (20:00/21:00) segons el README.
            # Un valor com "11 de la tarde" és incorrecte.
            if hora_num >= 1 and hora_num <= 9:
                hora_num = hora_num + 12
            else:
                return None # "las 11 de la tarde" cau aquí i retorna None
                
        elif franja == 'mañana':
            # 'mañana' accepta de l'1 a l'11. Les 12 de la mañana sol ser migdia.
            if hora_num == 12:
                hora_num = 12
            elif hora_num > 11:
                return None

        # El teu control clàssic preferit amb len()
        hora_final = str(hora_num)
        if len(hora_final) == 1: 
            hora_final = "0" + hora_final
            
        return f"{hora_final}:00"

    return None

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)