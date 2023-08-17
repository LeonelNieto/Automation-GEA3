"""
Módulo que contiene funciones especiales.
"""
from ATErds import Write
from Erd_List import Erd_Reset

def ResetUnit(dst="C0", board=1, Path=""):
    Write(dst, Erd_Reset, "01", Path, board)