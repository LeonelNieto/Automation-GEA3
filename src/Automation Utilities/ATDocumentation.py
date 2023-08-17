"""
Este módulo realiza la documentación automatica, agregando 
PASS and DONE, además de agregar el valor hexadecimal del ERD
"""
import re
from Erd_List import *

erd_dict = {key: value for key, value in locals().items() if key.startswith('Erd_')}

def AutoDocumentation(texto:str) -> None:
    """
    Función para documentar automáticamente los tickets
    
    Args:
        texto (str): Texto que se quiere documentar
        
    return:
        print() con el texto documentado
    """
    texto_modificado = re.sub(r'(?<=\b\w)(?=\b)', '- ', texto)
    for erd_nombre, erd_valor in erd_dict.items():
        erd_regex = re.compile(rf"\b{erd_nombre}\b")
        texto_modificado = erd_regex.sub(erd_nombre + " (0x" + erd_valor + ")", texto_modificado)

    lineas = texto_modificado.split('\n')
    for i in range(len(lineas)):
        if lineas[i].startswith('Read') or lineas[i].startswith('Verify'):
            lineas[i] += ' **-->PASS**'
        else:
            lineas[i] += ' **-->DONE**'

    texto_modificado = '\n'.join(lineas)
    print(texto_modificado)