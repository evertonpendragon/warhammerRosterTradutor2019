# encoding: utf-8
# encoding: iso-8859-1
# encoding: win-1252
# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import os
import json
import zipfile as zip
from shutil import copyfile
from bs4 import BeautifulSoup
from googletrans import Translator
translator = Translator()
########################################################################################################################
# Lê os arquivos cat da pasta wh40k-master, traduz utilizando o dicionário e
# gera os arquivos catz prontos para serem importados no Battlescribe
########################################################################################################################

def compactCat(ppath):
    print '\n\n\n\n',  'Compactando arquivo'
    os.chdir(ppath)
    destCatFiles = os.listdir('.')
    destCatFiles = filter(lambda x: x[-1] != 'z', destCatFiles)
    for f in destCatFiles:
        print f
        compression = zip.ZIP_DEFLATED
        with zip.ZipFile(f+'z', mode='w') as zip_ref:
            zip_ref.write( f, compress_type=compression)
            zip_ref.close()
        os.remove(f)


originPath = "./wh40k-master/"
destPath = "./wh40k_PTBR-master/"

if not os.path.exists(destPath):
    os.makedirs(destPath)

for f in os.listdir(originPath):
    originFileFullPath = originPath+f
    PTBR_file = f.replace(' ', '_').replace(',','.').replace('\'','')
    PTBR_zfile = PTBR_file + 'z'

    destFileFullPath = destPath + PTBR_file
    if os.path.splitext(originFileFullPath)[1] in [".catz",'.gstz']:
        with zip.ZipFile(f, 'r') as zip_ref:
            zip_ref.extractall(destPath)
    elif os.path.splitext(originFileFullPath)[1] in ['.cat', '.gst']:
        copyfile(originFileFullPath, destFileFullPath)
    else:
        continue


#catz = filter(lambda x: 'Wolves.cat' in x, catz) #filtra somente um arquivo dos sparce wolves

with open('dicionario.json', "r") as file:
    dicionario = json.loads(file.read())
    file.close()

catz = os.listdir(destPath)
for cfile in catz:
    destCatFileName = destPath + cfile
    with open(destCatFileName, "r") as file:
        catFile = file.read()
        file.close()
    cat = BeautifulSoup(catFile, "xml")
    #print catFile


    if 1==1: #filtro para debbug
        # TRADUZ ARQUIVO CAT
        for catalogues in cat.find_all("catalogue"):
            catalogues["name"] += "-PTBR"
            for catalogue in catalogues.children:
                # print catalogue.name, type(catalogue)
                if catalogue.name <> None:
                    print 'n1', catalogue.name
                    if catalogue.name in ["sharedrules", "sharedprofiles", "selectionentries", "sharedselectionentries",
                                          "sharedselectionentrygroups","sharedRules","sharedProfiles","sharedSelectionEntryGroups",
                                          "sharedSelectionEntries","selectionEntries"]:
                        for catElement in catalogue.children:
                            if catElement.name <> None:
                                for ruleTag in catElement.find_all("description"):
                                    rule = ruleTag.get_text()  #
                                    # print rule
                                    if rule in dicionario.keys() and len(rule) > 1:
                                        rulePT = dicionario[rule]
                                        print "Traduzindo>>>", cfile,"\n", rule, "\n", rulePT
                                        #print type(cat)
                                        try:
                                            #cat.find(text=rule).replaceWith(rulePT)
                                            ruleTag["description"]=rulePT
                                        except Exception:
                                            print "falha na traducao"
                                            sys.exc_clear()

                                    else:
                                        print "Nao existe no dicionario", rule

                                for characteristicsTag in catElement.find_all("characteristic"):
                                    if characteristicsTag["name"] in ["Abilities", "Description"]:
                                        # print profiles["name"],   characteristic["name"], characteristic["value"],characteristic

                                        #print characteristicsTag

                                        if characteristicsTag.has_attr('value'):
                                            description = characteristicsTag["value"]
                                            #print description
                                            if description in dicionario.keys() and len(description) > 1:
                                                descriptionPT =dicionario[description]
                                                # print "adicionando", description
                                                print "Traduzindo>>>", cfile,"\n", description, "\n", descriptionPT
                                                #print type(cat)
                                                try:
                                                    #cat.find(text=description).replaceWith(descriptionPT)

                                                    characteristicsTag["value"]=descriptionPT
                                                except Exception:
                                                    print "falha na traducao"
                                                    sys.exc_clear()
                                            else:
                                                print "nao existe no dicionario", description


        # TRADUS ARQUIVO GST
        for catalogues in cat.find_all("gameSystem"):
            catalogues["name"] += "-PTBR"
            for catalogue in catalogues.children:
                # print catalogue.name, type(catalogue)
                if catalogue.name <> None:
                    print 'n1', catalogue.name
                    if catalogue.name in ["sharedrules", "sharedprofiles", "selectionentries", "sharedselectionentries",
                                          "sharedselectionentrygroups","sharedRules","sharedProfiles","sharedSelectionEntryGroups",
                                          "sharedSelectionEntries","selectionEntries",""]:
                        for catElement in catalogue.children:
                            if catElement.name <> None:
                                for ruleTag in catElement.find_all("description"):
                                    rule = ruleTag.get_text()  #
                                    # print rule
                                    if rule in dicionario.keys() and len(rule) > 1:
                                        rulePT = dicionario[rule]
                                        print "Traduzindo>>>", cfile,"\n", rule, "\n", rulePT
                                        #print type(cat)
                                        try:
                                            #cat.find(text=rule).replaceWith(rulePT)
                                            ruleTag["description"]=rulePT
                                        except Exception:
                                            print "falha na traducao"
                                            sys.exc_clear()

                                    else:
                                        print "Nao existe no dicionario", rule

                                for characteristicsTag in catElement.find_all("characteristic"):
                                    if characteristicsTag["name"] in ["Abilities", "Description"]:
                                        # print profiles["name"],   characteristic["name"], characteristic["value"],characteristic

                                        #print characteristicsTag

                                        if characteristicsTag.has_attr('value'):
                                            description = characteristicsTag["value"]
                                            #print description
                                            if description in dicionario.keys() and len(description) > 1:
                                                descriptionPT =dicionario[description]
                                                # print "adicionando", description
                                                print "Traduzindo>>>", cfile,"\n", description, "\n", descriptionPT
                                                #print type(cat)
                                                try:
                                                    #cat.find(text=description).replaceWith(descriptionPT)

                                                    characteristicsTag["value"]=descriptionPT
                                                except Exception:
                                                    print "falha na traducao"
                                                    sys.exc_clear()
                                            else:
                                                print "nao existe no dicionario", description



    print '\n\n\n\n', cfile, 'Tradução Finalizada'
    #print cat
    newFile = destCatFileName
    xml = cat.prettify("utf-8")
    with open(newFile, "wb") as file:
        file.write(xml)
        file.close()

#compacta
compactCat(destPath)