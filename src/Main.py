# /***********************************************************************/
# /*                                                                     */
# /*  FILE          : Main.py                                            */
# /*  DATE          : 17/02/2023                                         */
# /*  DESCRIPTION   : Serial GEA3                                        */
# /*                                                                     */
# /*  AUTHOR        : Leonel Nieto Lara                                  */
# /*                                                                     */
# /*  PROJECT       : GEA3 Tool                                          */
# /*  IDE           : Visual Studio Code                                 */
# /*  Python Version: 3.10.11                                             */
# */                                                                     */
# /*  Copyright 2012-2023 Mabe TyP                                       */
# /*  All rights reserved                                                */
# /*                                                                     */
# /***********************************************************************/
from Markdown import Init
Init()
from ReadorWrite import ReadErd, WriteErd, Bootloader
from verifylength import longitudERD
import serial
import serial.tools.list_ports

# /************************************************************************
#  Name:          SetBoard()    
#  Parameters:    Board
#  Returns:       N/A
#  Called by:     LabVIEW
#  Calls:         N/A
#  Description:   Configure serial port to GEA3, conceting to serial com
#                 with the board through LabVIEW, and define global ser  
#                 to use to write and read frames.
#               
# ************************************************************************/
def SetBoard(board):                                                                    # Función para configurar el puerto COM
    global ser
    ser = serial.Serial()
    ser.baudrate = 230400                                                               # Baudrate para GEA3
    ser.bytesize = serial.EIGHTBITS
    ser.parity = serial.PARITY_NONE                                                          
    ser.timeout = 0.5                                                                   # Timeout 500 ms si no responde
    com_ports = list(serial.tools.list_ports.comports())                                # Crea una lista para los puertos disponibles
    ser.port = com_ports[board].device                                                  # Se define el puerto a través de LabVIEW
    ser.open()                                                                          # Abre puerto COM

# /************************************************************************
#  Name:          ReadButton( )    
#  Parameters:    Destination (str), ERD (str)
#  Returns:       Data read (str)
#  Calls:         verifylength.longitudERD( )
#                 ReadorWrite.ReadErd( )
#  Description:   Write a frame to read a serial, and return a complete
#                 frame read until reach bit stop.
#               
# ************************************************************************/                                         
def ReadFrame(dst:str, ERD:str) -> str:                                 
    Erd = longitudERD(ERD).upper()             
    while True:
        complete_frame = ""  
        lectura = ReadErd(Erd, dst)        
        ser.write(lectura)                                       
        while True:
            reading = ser.read(1)                 
            concatenate = reading.hex()                                     
            complete_frame += concatenate                                        
            if reading == b'\xE3':                               
                break                   
            if reading == b'':   
                complete_frame = "Verifica conexiones"   
                break
        complete_frame = complete_frame.upper()          
        Byte_ERD = complete_frame[14:18]
        Byte_OK = complete_frame[12:14]
        if (Byte_ERD == Erd) and (Byte_OK == "00"):
            Longitud_Dato_hex = complete_frame[18:20]
            Longitud_Dato_int = int(Longitud_Dato_hex, 16) * 2
            Dato = complete_frame[20:(20 + Longitud_Dato_int)]
            break
    return Dato                                                       # Retorna la trama o mensajes de error.

SetBoard(1)
print(ReadFrame("C0", "003a"))
# /************************************************************************
#  Name:          WriteButton( )    
#  Parameters:    Destination, ERD, dato
#  Returns:       Frame read
#  Calls:         verifylength.longitudERD( )
#                 ReadorWrite.WriteErd( )
#  Description:   Write a frame to write a serial, and read the frame that 
#                 MC respond to return a complete frame read until 
#                 reach bit stop.
#               
# ************************************************************************/
def WriteFrame(dst, ERD, dato):                                                     # Función para escirbir al ERD, con argumentos; Destination, ERD y dato 
    complete_frame = ""                                                             # Se inicia el strign de la trama vacío
    dato = dato.replace(" ", "")                                                    # Se eliminan espacios en el argumento dato
    longitudERD = longitudERD(ERD)                                                  # Verifica la longitud del ERD y agrega 0s si es menor a 4 si es mayor retorna error
    if longitudERD == "Fallo":                                                      # Si la longitud es mayor a 5 envía Fallo
        complete_frame = "Error"                                                    # Retorna Error
    else:
        escritura = WriteErd(longitudERD, dato, dst)                                # Completa la trama con el ERD, Destination y dato a escribir dado por LabVIEW
        ser.write(escritura)                                                        # Se escribe la trama por serial
        while True:
            reading = ser.read(1)                                                   # Se lee el primer byte
            concatenate = reading.hex()                                             # Se convierte a hexadecimal la lectura serial
            complete_frame += concatenate                                           # Se concatena byte por byte
            if reading == b'\xE3':                                                  # Si se lee el bit de Stop
                break                                                               # Sale del ciclo while
            if reading == b'':                                                      # Si no lee nada
                break                                                               # Sale del ciclo while
        BitInicio = complete_frame[0:2]                                             # Toma los dos primeros valores
        if BitInicio != "e2":                                                       # Verifica que no sea el bit de inio
            complete_frame = "Error"                                                # Si no es manda Error
        else:                                                                       # Si es el bit de inio
            complete_frame = complete_frame[2: ]                                    # Manda la trama de datos sin el bit de inicio
        return complete_frame                                                       # Retorna la trama

# /************************************************************************
#  Name:          WriteBootloader( )    
#  Parameters:    Destination, command, message
#  Returns:       Frame read
#  Called by:     LabVIEW
#  Calls:         ReadorWrite.Boatloader( )
#  Description:   Write a frame to write a serial message, and read
#                 the frame that MC respond to return a complete frame 
#                 read until reach bit stop.
#               
# ************************************************************************/
def WriteBootloader(dst, command, message):                                             # Función para escribir mensajes con lo argumentos Destination, Comando y Mensaje.
    CompleteFrame = "" 
    dst = str(dst)
    command = str(command)
    message = str(message)
    lectura = Bootloader(dst, command, message)                                         # Concatenación de la trama completa a escribir
    ser.write(lectura)                                                                  # Escribe la trama al puerto serial
    reading = (ser.read()).hex()                                                        # Lee el primer byte de datos y lo convierte a hexadecimal
    if reading != "e2":                                                                 # Si el primer byte no es el byte de inicio
        CompleteFrame = "Error"
    else:                                                                               # Si el primer byte leido es el de Inicio
        while (1):
            reading = (ser.read()).hex()                                                # Lee byte por byte y lo convierte a hexadecimal 
            CompleteFrame += reading                                                    # Concatenación de bytes
            if reading == "":                                                           # Si no lee nada sale del ciclo
                break
            elif reading == "e3":                                                       # Si detecta el byte de paro sale del ciclo
                break 
    Mensaje = CompleteFrame.upper()                                                     # Convierte la trama a Mayusculas
    return Mensaje                                                                      # Retorna la trama o mensaje de error

