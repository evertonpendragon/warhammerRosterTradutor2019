# encoding: utf-8
# encoding: iso-8859-1
# encoding: win-1252
# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import os
import json

from bs4 import BeautifulSoup
from googletrans import Translator
translator = Translator()
########################################################################################################################
# traduz um arquivo de roster no formato html
########################################################################################################################

#translator = Translator(service_urls=['translate.google.com','translate.google.co.kr'])

with open('dicionario.json', "r") as file:
    dicionario = json.loads(file.read())

for file in os.listdir("."):
    if file.endswith(".html") and not os.path.splitext(file)[0].endswith("-PTBR"):
        print type(file), file
        f = open (file,"r")
        htmlDoc = f.read()
        f.close()

        soup = BeautifulSoup(htmlDoc, 'html.parser')

        texts = soup.find_all("td")

        texts = [x.get_text() for x in texts]

        #texts = soup.get_text()
        print texts
        #texts = soup.get_text().split('\n')
        #print texts
        #texts = [x.strip() for x in texts]
        #print texts
        #texts = filter(None, texts)
        for text in texts:
            if text in dicionario.keys():
                print text
                soup.find(text=text).replaceWith(dicionario[text])

        #salvando documento traduzido
        newFile = os.path.splitext(file)[0] + "-PTBR.html"
        html = soup.prettify("utf-8")
        with open(newFile, "wb") as file:
            file.write(html)

# if abilityPT<>"" and  abilityPT <> ability:
 #          print "traduzindo ",ability,"->",abilityPT
 #          soup.find(text=ability).replaceWith(abilityPT)

 #     if descriptionPT <> "" and descriptionPT <> description:
 #          print "traduzindo ", description, "->", descriptionPT
 #          soup.find(text=description).replaceWith(descriptionPT)

 #      #salvando documento traduzido
 #      newFile = os.path.splitext(file)[0] + "-PTBR.html"
 #      html = soup.prettify("utf-8")
 #      with open(newFile, "wb") as file:
 #           file.write(html)

