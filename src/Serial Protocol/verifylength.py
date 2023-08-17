# /***********************************************************************/
# /*                                                                     */
# /*  FILE          : verifylength.py                                    */
# /*  DATE          : 17/02/2023                                         */
# /*  DESCRIPTION   : Calculate ERD length                               */
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

# /************************************************************************
#  Name:          longitudERD   
#  Parameters:    ERD
#  Returns:       Complete length or ERD
#                 Fallo
#  Called by:     ReadButton( ) from (Main.py)
#                 WriteButton( ) from (Main.py)
#  Calls:         N/A
#  Description:   Complete the ERD with 0's in the left if lenght is
#                 less than 4, if length is 4 return the same
#                 ERD, else return "Fallo"
#               
# ************************************************************************/
def longitudERD(ERD):
    numeroCaracteres = len(ERD)                        # Obtiene el número de caracteres del ERD
    return {                                           # Diccionario para retornar valores deacuerdo a la longitud
        1 : "000" + ERD,                               # Longitud del ERD = 1, se agregan tres 0's a la izquierda
        2 :  "00" + ERD,                               # Longitud del ERD = 2, se agregan dos 0's a la izquierda
        3 :   "0" + ERD,                               # Longitud del ERD = 3, se agregan un 0 a la izquierda
        4:          ERD                                # Longitud del ERD = 4, el ERD se queda igual
    }.get(numeroCaracteres, "Fallo")                   # No detecta ningún valor, retorna fallo
