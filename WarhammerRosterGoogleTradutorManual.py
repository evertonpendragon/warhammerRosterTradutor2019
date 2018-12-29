# encoding: utf-8
# encoding: iso-8859-1
# encoding: win-1252
# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import os
#import json

from bs4 import BeautifulSoup
from googletrans import Translator
translator = Translator()

#translator = Translator(service_urls=['translate.google.com','translate.google.co.kr'])


dicionario={}
#and ability not in dicionario.keys():
for file in os.listdir("."):
    if file.endswith(".html") and not os.path.splitext(file)[0].endswith("-PTBR"):
         print type(file), file
         f = open (file,"r")
         htmlDoc = f.read()
         f.close()


         soup = BeautifulSoup(htmlDoc, 'html.parser')


         for table in soup.find_all('table'):

               #table = soup.find_all('table')[5]
               #print table
               cIndex=0
               descriptionIndex = 0
               abilitiesIndex = 0
               for row in table.findAll('tr'):
                    for c in row.findAll('th'):
                         if c.contents[0] == "Description":
                              descriptionIndex = cIndex
                         if c.contents[0] == "Abilities":
                              abilitiesIndex = cIndex
                         cIndex += 1

               #print abilitiesIndex, descriptionIndex


               for row in table.findAll('tr'):
                    descriptionPT = ""
                    abilityPT = ""
                    columns = row.findAll('td')
                    if columns :
                        # print columns
                        ability = row.findAll('td')[abilitiesIndex].contents[0]
                        description = row.findAll('td')[descriptionIndex].contents[0]

                        #traduz
                        if ability.split().__len__()>4 and ability not in dicionario.keys():
                             abilityPT = translator.translate(ability, dest='pt').text
                        else:
                             abilityPT =ability

                        if description.split().__len__() > 4 and description not in dicionario.keys():
                             descriptionPT = translator.translate(description, dest='pt').text
                        else:
                             descriptionPT=descriptionPT
                        #print description,descriptionPT
                        #print ability, abilityPT

                        if abilityPT<>"" and  abilityPT <> ability:
                             print "traduzindo ",ability,"->",abilityPT
                             dicionario[ability]=abilityPT

                        if descriptionPT <> "" and descriptionPT <> description:
                             print "traduzindo ", description, "->", descriptionPT
                             dicionario[description] = descriptionPT
         #salvando documento traduzido

    #     newFile = "dicionario.json"
    #     with open(newFile, "wb") as file:
    #          file.write(json.dumps(dicionario,indent=4, sort_keys=True, ensure_ascii=False))
#
