# encoding: utf-8
# encoding: iso-8859-1
# encoding: win-1252
# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import os
import json

j={}
dFile = "teste.txt"
with open(dFile, "wb") as file:
    for i in range(1,10):
        file.writelines(str(i))
