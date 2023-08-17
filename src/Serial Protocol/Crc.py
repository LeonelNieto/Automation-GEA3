# /***********************************************************************/
# /*                                                                     */
# /*  FILE          : Crc.py                                             */
# /*  DATE          : 17/02/2023                                         */
# /*  DESCRIPTION   : CRC Calcultaor                                     */
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

# ***********************************************************************************************
#  Name:          crc16_ccitt(data_hex)    
#  Parameters:    data_hex
#                 Data to calculate CRC Frame
#                 Data =  dst + length + src + cmd + ERD 
#  Returns:       Crc16 CCITT
#  Called by:     ReadERD( )
#                 WriteERD( )
#                 Boatloader( )
#  Calls:         N/A
#  Description:   Calculate CRC16 CCITT for complete the frome to write at the serial.  
#               
# ***********************************************************************************************
def crc16_ccitt(data_hex):
    data = bytearray.fromhex(data_hex)                                      # Convierte la trama recibida a bytearray hexadecimal
    poly = 0x1021                                                           # poly 1021
    crc = 0x1021                                                            # Valor inicial 1021
    for byte in data:
        for i in range(8):
            bit = (byte >> (7-i) & 1) == 1
            c15 = (crc >> 15 & 1) == 1
            crc <<= 1
            if c15 ^ bit:
                crc ^= poly
    crc &= 0xffff
    crcStr = "{:04x}".format(crc)
    
    return crcStr

############## Datos Para Calcular CRC lectura ###################

### dst ### length ### src ###    cmd    ###   ERD    ###  
#    C0       XX        E4       XX XX        XX XX             
