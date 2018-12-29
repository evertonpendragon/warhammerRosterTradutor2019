# encoding: utf-8
# encoding: iso-8859-1
# encoding: win-1252
# encoding=utf8

########################################################################################################################
# Le o arquivo cat e traduz com o google tradutor
########################################################################################################################

import sys
reload(sys)
sys.setdefaultencoding('utf8')
import json
from bs4 import BeautifulSoup
from googletrans import Translator
translator = Translator()

filesToRead = ["./wh40k-master/Imperium - Space Marines.cat", "./wh40k-master/Imperium - Space Wolves.cat"]

for catFilesToRead in filesToRead:
    catFile = open(catFilesToRead)
    cat = BeautifulSoup(catFile, "lxml")

    with open('dicionario.json', "r") as file:
        dicionario =  json.loads(file.read() )


    #dicionario={}

    for catalogues in cat.find_all("catalogue"):
        for catalogue in catalogues.children:
            #print catalogue.name, type(catalogue)
            if catalogue.name <> None:
                print 'n1',catalogue.name
                if catalogue.name in ["sharedrules","sharedprofiles"]:
                    for catElement in catalogue.children:
                        if catElement.name <> None:
                            #print 'n2\t',catElement.name
                            #print '____'
                            #print "desc",catElement.description
                            #print '____'
                            for ruleTag in catElement.find_all("description"):
                                rule = ruleTag.get_text()#
                                #print rule
                                if rule not in dicionario.keys() and len(rule) > 1:
                                    rulePT = translator.translate(rule, dest='pt').text
                                    print "Traduzindo>>>\n",rule,"\n",rulePT
                                    dicionario[rule] = rulePT
                                else:
                                    print "ja existe no dicionario", rule

                            for characteristicsTag in catElement.find_all("characteristic"):
                                if characteristicsTag["name"] in["Abilities", "Description"]:
                                        #print profiles["name"],   characteristic["name"], characteristic["value"],characteristic
                                        description=characteristicsTag["value"]
                                        print description
                                        if description not in dicionario.keys() and len(description) > 1:
                                            descriptionPT = translator.translate(description, dest='pt').text
                                            #print "adicionando", description
                                            print "Traduzindo>>>\n", description, "\n", descriptionPT
                                            dicionario[description] = descriptionPT
                                        else:
                                            print "ja existe no dicionario", description



    newFile = "dicionario.json"
    with open(newFile, "wb") as file:
        file.write(json.dumps(dicionario,indent=4, sort_keys=True, ensure_ascii=False))

    # print 'n3\t\t',catElement.contents[9]
    # profile= catElement.contents[9]
    # print type(profile)
    # for rule in profile.find_all("rule"):
    #     print rule
    # for characteristic in profile.find_all("characteristic"):
    #     if characteristic["name"] in["Abilities", "Description"]:
    #         #print profiles["name"],   characteristic["name"], characteristic["value"],characteristic
    #         description=characteristic["value"]
    #         if description not in dicionario.keys():
    #
    #             #print "adicionando", description
    #             dicionario[description] = ""
    #         #else:
    #         #    print "ja existe", description
