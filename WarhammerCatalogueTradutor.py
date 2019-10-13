# encoding: utf-8
# encoding: iso-8859-1
# encoding: win-1252
# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import os
from shutil import copyfile
import json
import requests
import zipfile as zip
from shutil import copyfile,rmtree
from bs4 import BeautifulSoup
from googletrans import Translator
import DataIndexer as dtIdx

translator = Translator()
########################################################################################################################
# Faz download do repositório oficial
# Lê os arquivos cat da pasta wh40k-master, traduz utilizando o dicionário e
# gera os arquivos catz prontos para serem importados no Battlescribe
# Passo 2: Criar o repositorio com o BS clicando em share my data
# Passo 3: C:\Users\evert\Documents\GitHub\BSDataBrasil\
########################################################################################################################

def translate(text,dest):
    textTransl=''
    if text not in ('', '0', '-'):
        try:
            print "Traduzindo no google >>>\n", text,type(text), "\n", textTransl

            textTransl = translator.translate(text, dest=dest).text
            return textTransl
        except Exception,e:
            print "Falha na traducao do Google, {exception}, {e}".format(exception=Exception.message,e=str(e))
            sys.exc_clear()
            return text


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
def copyCatToRepoDir(ppath, destPath):
    print '\n\n\n\n',  'Copiando para diretorio do repositorio'
    #os.chdir(ppath)
    destCatFiles = os.listdir(ppath)
    destCatFiles = filter(lambda x: x[-1] != 'z', destCatFiles)

    for f in destCatFiles:
        print 'copiando arquivo', ppath+f, ' ', destPath+f
        copyfile(ppath+f, destPath+f)

def downloadWh40kSource():
    r = requests.get('https://github.com/BSData/wh40k/archive/master.zip')
    open('wh40k-master.zip', 'wb').write(r.content)
    print 'Download completo'
    with zip.ZipFile('./wh40k-master.zip', mode='r') as zip_ref:
        zip_ref.extractall(path='.')
    print 'Arquivos extraídos'

def translateText(description,dicionario):
    #description=description.upper()
    if description.upper() in dicionario:
        descriptionPT = dicionario[description]
    elif description not in ('','0','-'):
        #description.replace("","'") in dicionario
        print "Texto nao encontrado no dic {t}".format(t=description)
        descriptionPT=description
    return descriptionPT

########################################################################################################################

originPath = "./wh40k-master/"
destPath = "./wh40kBR-master/"
catRepoDir = 'C:/Users/evert/Documents/GitHub/BSDataBrasil/wh40kBR/'
projectDir= 'C:/Users/evert/Documents/PycharmProjects/WarhammerRosterTradutor/'




gameSystemId='49b6-bc6f-0390-1e40'

print 'Download do repositório de origem'
downloadWh40kSource()

if os.path.exists(destPath):
    rmtree(destPath, True)


if not os.path.exists(destPath):
    os.makedirs(destPath)

for f in os.listdir(originPath):
    originFileFullPath = originPath+f
    BR_file = f.replace(' ', '_').replace(',','.').replace('\'','')
    BR_zfile = BR_file + 'z'

    destFileFullPath = destPath + BR_file
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

dicionario = {k.upper():v for k,v in dicionario.items()}
dicionarioNew = {}

naoLocalizados=0
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
            catalogues["name"] += "-BR"

            catalogues["gameSystemId"] = gameSystemId

            for catalogue in catalogues.children:
                # print catalogue.name, type(catalogue)
                if catalogue.name <> None:
                    #print 'n1', catalogue.name
                    if catalogue.name in ["sharedrules", "sharedprofiles", "selectionentries", "sharedselectionentries",
                                          "sharedselectionentrygroups","sharedRules","sharedProfiles","sharedSelectionEntryGroups",
                                          "sharedSelectionEntries","selectionEntries"]:
                        for catElement in catalogue.children:
                            if catElement.name <> None:
                                for ruleTag in catElement.find_all("description"):
                                    rule = ruleTag.get_text() .upper() #
                                    # print rule
                                    if rule.upper() in dicionario.keys() and len(rule) > 1:
                                        rulePT = dicionario[rule]
                                        #print "Traduzindo>>>", cfile,"\n", rule, "\n", rulePT
                                        #print type(cat)
                                        try:
                                            #cat.find(text=rule).replaceWith(rulePT)
                                            #ruleTag["description"]=rulePT
                                            ruleTag.string=rulePT

                                        except Exception:
                                            print "falha na traducao"
                                            sys.exc_clear()

                                    else:
                                        if rule <> '-' and rule <> "" and rule <> " " and type(rule)<>None:
                                            if rule <> "":
                                                print "Nao existe no dicionario", rule
                                                textPT = translate(ruleTag.get_text(), dest='pt')
                                                dicionarioNew[rule]=textPT
                                                naoLocalizados += 1

                                for characteristicsTag in catElement.find_all("characteristic"):
                                    if characteristicsTag["name"] in ["Abilities", "Description","Details","Capacity"]:
                                        # print profiles["name"],   characteristic["name"], characteristic["value"],characteristic

                                        #print characteristicsTag.text

                                        #if characteristicsTag.has_attr('value')  :#removido na versao 2, 13/06/2019
                                        #description = characteristicsTag["value"] #removido na versao 2, 13/06/2019
                                        description = characteristicsTag.text.upper() #linhas foram recuadas pq  if de cima foi removido #if characteristicsTag.has_attr('value')
                                        #print description
                                        if description.upper() in dicionario.keys() and len(description) > 1:
                                            descriptionPT =translateText(description,dicionario)#dicionario[description]
                                            # print "adicionando", description
                                            #print "Traduzindo>>>", cfile,"\n", description, "\n", descriptionPT
                                            #print type(cat)
                                            try:
                                                #cat.find(text=description).replaceWith(descriptionPT)

                                                #characteristicsTag["value"]=descriptionPT
                                                characteristicsTag.string = descriptionPT
                                                #print characteristicsTag.text
                                            except Exception, e:
                                                print "falha na traducao {e}".format(e=str(e))
                                                sys.exc_clear()
                                        else:
                                            if description <> '-' and description <> "":
                                                print "nao existe no dicionario", description
                                                if description<>"":
                                                    naoLocalizados+=1
                                                    textPT = translate(characteristicsTag.text, dest='pt')
                                                    dicionarioNew[description] = textPT


        # TRADUS ARQUIVO GST
        for catalogues in cat.find_all("gameSystem"):
            catalogues["name"] += "-BR"
            catalogues["gameSystemId"] = gameSystemId
            catalogues["id"] = gameSystemId
            for catalogue in catalogues.children:
                # print catalogue.name, type(catalogue)
                if catalogue.name <> None:
                    #print 'n1', catalogue.name
                    if catalogue.name in ["sharedrules", "sharedprofiles", "selectionentries", "sharedselectionentries",
                                          "sharedselectionentrygroups","sharedRules","sharedProfiles","sharedSelectionEntryGroups",
                                          "sharedSelectionEntries","selectionEntries",""]:
                        for catElement in catalogue.children:
                            if catElement.name <> None:
                                for ruleTag in catElement.find_all("description"):
                                    rule = ruleTag.get_text() .upper() #
                                    # print rule
                                    if rule.upper() in dicionario.keys() and len(rule) > 1:
                                        rulePT = dicionario[rule]
                                       # print "Traduzindo>>>", cfile,"\n", rule, "\n", rulePT
                                        try:
                                            #cat.find(text=rule).replaceWith(rulePT)
                                            #ruleTag["description"]=rulePT
                                            # ruleTag["description"]=rulePT
                                            ruleTag.string = rulePT
                                        except Exception:
                                            print "falha na traducao"
                                            sys.exc_clear()

                                    else:

                                        if description <> "":
                                            print "Nao existe no dicionario", rule
                                            naoLocalizados += 1
                                            textPT = translate(ruleTag.get_text(), dest='pt')
                                            dicionarioNew[rule] = textPT

                                for characteristicsTag in catElement.find_all("characteristic"):
                                    if characteristicsTag["name"] in ["Abilities", "Description","Details","Capacity"]:
                                        # print profiles["name"],   characteristic["name"], characteristic["value"],characteristic

                                        #print characteristicsTag

                                        if characteristicsTag.has_attr('value') or 1==1:
                                            #description = characteristicsTag["value"]
                                            description=characteristicsTag.text.upper()
                                            #print description
                                            if description.upper() in dicionario.keys() and len(description) > 1:
                                                descriptionPT =dicionario[description]
                                                #print "Traduzindo>>>", cfile,"\n", description, "\n", descriptionPT
                                                #print type(cat)
                                                try:
                                                    #cat.find(text=description).replaceWith(descriptionPT)

                                                    #characteristicsTag["value"]=descriptionPT
                                                    characteristicsTag.string = descriptionPT
                                                except Exception:
                                                    print "falha na traducao"
                                                    sys.exc_clear()
                                            else:
                                                if description<>"":
                                                    print "nao existe no dicionario", description
                                                    naoLocalizados+=1
                                                    textPT = translate(characteristicsTag.text, dest='pt')
                                                    dicionarioNew[description] = textPT



    print '', cfile, 'Tradução Finalizada'
    #print cat
    newFile = destCatFileName
    xml = cat.prettify("utf-8")
    with open(newFile, "wb") as file:
        file.write(xml)
        file.close()

#copia os arquivos cat para a pasta do repositorio
copyCatToRepoDir(destPath, catRepoDir)
#compacta
compactCat(destPath)


newFile = "{projectDir}dicionario_new.json".format(projectDir=projectDir)
with open(newFile, "wb") as file:
    file.write(json.dumps(dicionarioNew,indent=4, sort_keys=True, ensure_ascii=False))


print "Registros nao localizados no dicionario {i}".format(i=str(naoLocalizados))

dtIdx.createIndexBsr()
