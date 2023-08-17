import sys
import os

def Init():
    Executable_Path = sys.argv[0]
    sys.path.append(os.path.dirname(os.path.abspath(Executable_Path)) + "\Serial Protocol")
