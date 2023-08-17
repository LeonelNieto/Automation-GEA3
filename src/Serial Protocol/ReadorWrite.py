# /***********************************************************************/
# /*                                                                     */
# /*  FILE          : ReadorWrite.py                                     */
# /*  DATE          : 17/02/2023                                         */
# /*  DESCRIPTION   : Concatenate data frame                             */
# /*                                                                     */
# /*  AUTHOR        : Leonel Nieto Lara                                  */
# /*                                                                     */
# /*  PROJECT       : GEA3 Tool                                          */
# /*  IDE           : Visual Studio Code                                 */
# /*  Python Version: 3.9.13                                             */
# */                                                                     */
# /*  Copyright 2012-2023 Mabe TyP                                       */
# /*  All rights reserved                                                */
# /*                                                                     */
# /***********************************************************************/

import Crc

# /************************************************************************
#  Name:          ReadErd( )    
#  Parameters:    ERD, Destination
#  Returns:       Frame to write to the serial
#  Called by:     ReadButton( ) from (Main.py)
#  Calls:         crc16_ccitt( ) in (Crc.py)
#  Description:   Concatenate the frame to write for serial with GEA, usign
#                 BitInit, Destination, lenght, source, Command, CRC
#                 and bit Stop
#               
# ************************************************************************/
def ReadErd(ERD, dst):
    bitInit = "E2"                                                                                      # Bit de Inicio
    src = "E4"                                                                                          # Source
    cmd = "A000"                                                                                        # Comando de  request para lectura
    bitStop = "E3"                                                                                      # Bit de Stop
    longitud = int(((len(bitInit + dst + src + cmd + ERD + bitStop)) + 6) / 2)                          # Cálculo de la longitud de la trama
    lenght = "{:02x}".format(longitud)                                                                  # Conversión a hexadecimal de dos digitos
    FrameToCalculateCrc = dst + lenght + src + cmd + ERD                                                # Concatena trama para calculo de CRC
    crc = Crc.crc16_ccitt(FrameToCalculateCrc)                                                          # Calcula el CRC                                                                                   # Elimina "0x" del CRC
    frame = bitInit + FrameToCalculateCrc + crc + bitStop                                               # Concatena la trama de datos completa en hexadecimal
    data = bytes.fromhex(frame)                                                                         # Convierte los datos a bytes
    print(frame)
    return data                                                                                         # Retorna la trama a escribir en el serial

# /************************************************************************
#  Name:          WriteErd( )    
#  Parameters:    ERD, Dato, Destination
#  Returns:       Frame to write to the serial
#  Called by:     WriteButton( ) from (Main.py)
#  Calls:         crc16_ccitt( ) in (Crc.py)
#  Description:   Concatenate the frame to write for serial with GEA, usign
#                 BitInit, Destination, Lenght, Source, Command, ERD,  
#                 Dato Lenght, Dato, CRC and bit Stop
#               
# ************************************************************************/
def WriteErd(ERD, dato, dst):
    bitInit = "E2"                                                                                      # Bit de Inicio
    src = "E4"                                                                                          # Source
    cmd = "A200"                                                                                        # Comando de request para escritura
    ERD_Data_Size = int((len(dato)) / 2)                                                                # Calculo de la longitud del dato a escribir
    ERD_Data_Size = "{:02x}".format(ERD_Data_Size)                                                      # Conversión a hexadecimal de dos digitos
    ESC = "E0"                                                                                          # Bit de ESC
    bitStop = "E3"                                                                                      # Bit de paro
    longitud = int(((len(bitInit + dst + src + cmd + ERD + ERD_Data_Size + dato + bitStop)) + 6) / 2)   # Calculo de la longitud de la trama
    lenght = "{:02x}".format(longitud)                                                                  # Conversion de la longitud a hexadecimal de dos digitos
    FrameToCalculateCrc = dst + lenght + src + cmd + ERD + ERD_Data_Size + dato                         # Concatenacion de la trama para calcular el CRC
    crc = Crc.crc16_ccitt(FrameToCalculateCrc)                                                          # Modulo para calcular CRC                                                                        
    if ERD != "0032":                                                                                   # Si el ERD es diferente del de reset (0032)
        frame = bitInit + FrameToCalculateCrc + crc + bitStop                                           # Concatena la trama para escribir normalmente
    else:                                                                                               # Si el ERD es 0032
        frame = bitInit + FrameToCalculateCrc + ESC + crc + bitStop                                     # Se agrega el bit de ESC antes del CRC
    dataWrite = bytearray.fromhex(frame)                                                                # Conversion de la trama a bytearray
    return dataWrite                                                                                    # Retorna la trama a escribir en serial para escritura    

# /************************************************************************
#  Name:          Boatloader( )    
#  Parameters:    Destination, command, message
#  Returns:       Frame to write to the serial
#  Called by:     ReadButton( ) from (Main.py)
#  Calls:         crc16_ccitt( ) in (Crc.py)
#  Description:   Concatenate the frame to write for serial with GEA, usign
#                 BitInit, dst, lenght, src, cmd, message, CRC and bit Stop 
#               
# ************************************************************************/
def Boatloader(dst, cmd, msg):
    bitInit = "E2"                                                                                      # Bit de inicio
    src = "E4"                                                                                          # Source
    bitStop = "E3"                                                                                      # Bit de paro
    longitud = int(((len(bitInit + dst + src + cmd + msg + bitStop)) + 6) / 2)                          # Calculo del tamaño de la trama sin contar bytes especiales
    lenght = "{:02x}".format(longitud)                                                                # Conversión a hexadecimal de dos digitos
    FrameToCalculateCrc = dst + lenght + src + cmd + msg                                                # Concatena la trama para el calculo de CRC
    crc = Crc.crc16_ccitt(FrameToCalculateCrc)                                                          # Modulo para calcular CRC
    frame = bitInit + FrameToCalculateCrc + crc + bitStop                                               # Concatena la trama para el envío del mensaje serial
    data = bytes.fromhex(frame)                                                                         # Convierte a bytes la trama a enviar por serial
    return data                                                                                         # Retorna la trama a escribir en el serial

################################### TRAMA DE DATOS LECTURA ###############################################

### Bit Inicio ### dst ### length ### src ###    cmd    ###   ERD    ###   CRC    ### Bit Stop ###
#       E2          C0       XX        E4       XX XX        XX XX        XX XX          E3    ###
