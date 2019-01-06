# encoding: utf-8
# encoding: iso-8859-1
# encoding: win-1252
# encoding=utf8

########################################################################################################################
# Le o arquivo cat e traduz com o google tradutor
# gera o carquivo cat traduzido na pasta wh40kBR-master
########################################################################################################################

import sys
reload(sys)
sys.setdefaultencoding('utf8')
import json
from bs4 import BeautifulSoup
from googletrans import Translator
translator = Translator()
import os

#filesToRead = ["./wh40k-master/Imperium - Space Marines.cat", "./wh40k-master/Imperium - Space Wolves.cat", "./wh40k-master/Warhammer 40,000 8th Edition.gst"]
filesToRead = ["Imperium - Space Marines.cat", "Imperium - Space Wolves.cat", "Warhammer 40,000 8th Edition.gst"]

originPath = "./wh40k-master/"
destPath = "./wh40kBR-master/"

if not os.path.exists(destPath):
    os.makedirs(destPath)

catFiles = os.listdir(originPath)

#catFiles = filter(lambda x: x in filesToRead, catFiles)

catFiles = filter(lambda x: os.path.splitext(x)[1] in [".cat",".gst"], catFiles)


for catFilesToRead  in catFiles:
    with open(originPath+catFilesToRead) as catFile:
        print originPath + catFilesToRead

        x = catFile.read()
        catFile.close()
    cat = BeautifulSoup(x, "xml")

    with open('dicionario.json', "r") as file:
        dicionario = json.loads(file.read() )

    # traduz arquivo cat
    for catalogues in cat.find_all("catalogue"):
        for catalogue in catalogues.children:
            #print catalogue.name, type(catalogue)
            if catalogue.name <> None:
                #print 'n1',catalogue.name
                if catalogue.name in ["sharedrules", "sharedprofiles", "selectionentries", "sharedselectionentries",
                                          "sharedselectionentrygroups","sharedRules","sharedProfiles","sharedSelectionEntryGroups",
                                          "sharedSelectionEntries","selectionEntries"]:
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
                                    try:
                                        rulePT = translator.translate(rule, dest='pt').text
                                        print "Traduzindo>>>\n",rule,"\n",rulePT
                                        dicionario[rule] = rulePT
                                    except Exception:
                                        print "falha na traducao"
                                        sys.exc_clear()
                                else:
                                    print "ja existe no dicionario", rule

                            for characteristicsTag in catElement.find_all("characteristic"):
                                if characteristicsTag["name"] in["Abilities", "Description"]:
                                        #print profiles["name"],   characteristic["name"], characteristic["value"],characteristic
                                        if characteristicsTag.has_attr('value'):
                                            description=characteristicsTag["value"]
                                            print description
                                            if description not in dicionario.keys() and len(description) > 1:
                                                try:
                                                    descriptionPT = translator.translate(description, dest='pt').text
                                                    print "Traduzindo>>>\n", description, "\n", descriptionPT
                                                    #print "adicionando", description
                                                    dicionario[description] = descriptionPT
                                                except Exception:
                                                    print "falha na traducao"
                                                    sys.exc_clear()
                                            else:
                                                print "ja existe no dicionario", description


    # traduz o arquivo gst
    for catalogues in cat.find_all("gameSystem"):
        for catalogue in catalogues.children:
            #print catalogue.name, type(catalogue)
            if catalogue.name <> None:
                print 'n1',catalogue.name
                if catalogue.name in ["sharedrules", "sharedprofiles", "selectionentries", "sharedselectionentries",
                                          "sharedselectionentrygroups","sharedRules","sharedProfiles","sharedSelectionEntryGroups",
                                          "sharedSelectionEntries","selectionEntries"]:
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
                                    try:
                                        rulePT = translator.translate(rule, dest='pt').text
                                        print "Traduzindo>>>\n",rule,"\n",rulePT
                                        dicionario[rule] = rulePT
                                    except Exception:
                                        print "falha na traducao"
                                        sys.exc_clear()
                                else:
                                    print "ja existe no dicionario", rule

                            for characteristicsTag in catElement.find_all("characteristic"):
                                if characteristicsTag["name"] in["Abilities", "Description"]:
                                        #print profiles["name"],   characteristic["name"], characteristic["value"],characteristic
                                        if characteristicsTag.has_attr('value'):
                                            description=characteristicsTag["value"]
                                            print description
                                            if description not in dicionario.keys() and len(description) > 1:
                                                try:
                                                    descriptionPT = translator.translate(description, dest='pt').text
                                                    print "Traduzindo>>>\n", description, "\n", descriptionPT
                                                    #print "adicionando", description
                                                    dicionario[description] = descriptionPT
                                                except Exception:
                                                    print "falha na traducao"
                                                    sys.exc_clear()
                                            else:
                                                print "ja existe no dicionario", description


    newFile = "dicionario.json"
    with open(newFile, "wb") as file:
        file.write(json.dumps(dicionario,indent=4, sort_keys=True, ensure_ascii=False))

