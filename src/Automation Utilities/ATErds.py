"""
Módulo para automatizar realiar la lectura y escritura de ERDS,
y almacenarlos en un archivo excel
"""

from datetime import datetime
import Main
import FileCsv
import messagepopup
import time

def Read(dst:str, ERD:str, Expected_Data:str, Path="", board=1) -> list[str]:
    """
    Función que realiza la lectura de los ERDS y lo almacena en un archivo excel
    
    Args:
        dst           (str): Dirección de la tarjeta que se desea comunicar
        ERD           (str): ERD que se desea consultar
        Expected_Data (str): Valor que se espera recibir
        Path          (str): Dirección para crear el archivo csv (default '')
        board         (int): Selección del puerto COM (default 1)
        
    Returns:
        list[str]: Lista con la fecha, hora, 'READ', ERD, valor esperado, valor leido, '---', PASS/FAIL, comments
    
    Example
    --------
    >>> Read('C0', '0032', '00', 'C:/Users/LNLMEXID/', 0)
    ['25-07-2023', '11:37:49', 'READ', '0032', '00', '00', '---', 'PASS', '---']
    >>> Read('C0', 'F06A', '00', 'C:/Users/LNLMEXID/', 0)
    ['25-07-2023', '11:22:26', 'READ', 'F06A', '00', '02', '---', 'FAIL', '00 != 02']
    """
    Main.SetBoard(board)
    Time = datetime.now().strftime("%H:%M:%S")
    Dia = datetime.now().strftime("%d-%m-%Y")
    Data = Main.ReadErd(dst, ERD)
    Action = "READ"
    if Data == Expected_Data:
        Result = "PASS"
        Comments = "---"
    else:
        Result = "FAIL"
        if len(Data) != len(Expected_Data):
            lenData = str(int(len(Data) / 2))
            lenExpected_Data = str(int(len(Expected_Data) / 2))
            Comments = f"Lenght {Expected_Data} ({lenExpected_Data}) != " +\
                        f"{Data} ({lenData})"
        else:
            Comments = f"{Expected_Data} != {Data}"
    Write_Dato = "---" 
    Data_To_Write = [Dia, Time, Action, ERD, Expected_Data, Data, Write_Dato, Result, Comments]
    if len(Path) != 0:
        FileCsv.Write_Data_CSV(Path, Data_To_Write)
    Main.ser.close()
    print(Data_To_Write)
    return Data_To_Write
    
def Write(dst:str, ERD:str, Write_Dato:str, Path="", board=1) -> list[str]:
    """
    Función que realiza la escritura de los ERDS y lo almacena en un archivo excel
    
    Args:
        dst        (str): Dirección de la tarjeta que se desea comunicar
        ERD        (str): ERD que se desea consultar
        Write Data (str): Valor que se desea escribir al ERD
        Path       (str): Dirección para crear el archivo csv (default '')
        board      (int): Selección del puerto COM (default 1)
        
    Returns:
        list[str]: Lista con la fecha, hora, 'WRITE', ERD, '---', '---', Write_Dato, 'DONE', '---'
    
    Example
    --------
    >>> Write('C0', '0032', '01', 'C:/Users/LNLMEXID/', 0)
    ['25-07-2023', '11:37:49', 'WRITE', '0032', '---', '---', '01', 'DONE', '---']
    """
    Main.SetBoard(board)
    time.sleep(0.3)
    Time = datetime.now().strftime("%H:%M:%S")
    Dia = datetime.now().strftime("%d-%m-%Y")
    Main.WriteButton(dst, ERD, Write_Dato)
    Action = "WRITE"
    Expected_Data = "---"
    Result = "DONE"
    Data = "---"
    Comments = "---"
    Data_To_Write = [Dia, Time, Action, ERD, Expected_Data, Data, Write_Dato, Result, Comments]
    if len(Path) != 0:
        FileCsv.Write_Data_CSV(Path, Data_To_Write)
    time.sleep(3.4)
    print(Data_To_Write)
    Main.ser.close()
    return Data_To_Write

def ActionPassOrFail(ToDo, Path=""):
    Time = datetime.now().strftime("%H:%M:%S")
    Dia = datetime.now().strftime("%d-%m-%Y")
    ACTION = "To Do"
    Expected_Data = ToDo
    ERD = "---"
    Result = messagepopup.ActionToDo(ToDo)
    Data = "---"
    Comments = "---"
    Write_Dato = "---"
    Data_To_Write = [Dia, Time, ACTION, ERD, Expected_Data, Data, Write_Dato, Result, Comments]
    if len(Path) != 0:
        FileCsv.Write_Data_CSV(Path, Data_To_Write)
    print(Data_To_Write)
    return Data_To_Write

def ToDoTimedAction(WaitSeconds:int, TextAction:str, Path="", LessTime=0):
    Time = datetime.now().strftime("%H:%M:%S")
    Dia = datetime.now().strftime("%d-%m-%Y")
    ACTION = TextAction
    Expected_Data = "---"
    ERD = "---"
    Result = "DONE"
    Data = "---"
    Comments = "---"
    Write_Dato = "---"
    messagepopup.TimedAction(WaitSeconds, TextAction, LessTime)
    Data_To_Write = [Dia, Time, ACTION, ERD, Expected_Data, Data, Write_Dato, Result, Comments]
    if len(Path) != 0:
        FileCsv.Write_Data_CSV(Path, Data_To_Write)
    print(Data_To_Write)
    return Data_To_Write

def ActionDone(Action:str, Path=""):
    Time = datetime.now().strftime("%H:%M:%S")
    Dia = datetime.now().strftime("%d-%m-%Y")
    ACTION = Action
    Expected_Data = "---"
    ERD = "---"
    Result = "DONE"
    Data = "---"
    Comments = "---"
    Write_Dato = "---"
    messagepopup.ImmediateAction(Action)
    Data_To_Write = [Dia, Time, ACTION, ERD, Expected_Data, Data, Write_Dato, Result, Comments]
    if len(Path) != 0:
        FileCsv.Write_Data_CSV(Path, Data_To_Write)
    print(Data_To_Write)
    return Data_To_Write