import xml.etree.cElementTree as ET
import xml.dom.minidom  as minidom
from bs4 import BeautifulSoup
def prettify(  elem ):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, encoding='UTF-8', method='xml')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t" , newl="\n",encoding='UTF-8'  )


class DataIndexer():
    def __init__(self):
        self.data = []

    def indexInitializer(self):
        dataIndex = ET.Element("dataIndex" )
        dataIndex
        dataIndex.attrib["battleScribeVersion"]="2.01"
        dataIndex.attrib["name"] = "wh40kPTBR"
        dataIndex.attrib["indexUrl"] = "https://github.com/evertonpendragon/wh40kBR/releases/download/v0.1.4/wh40kBR.bsi"
        dataIndex.attrib["xmlns"] = "http://www.battlescribe.net/schema/dataIndexSchema"
        return dataIndex
    def indexRepositoryUrls( self, dataIndex ):
        repositoryUrls = ET.SubElement(dataIndex, "repositoryUrls")
        #return repositoryUrls

    def indexDataIndexEntries(self,dataIndex ):
        dataIndexEntries = ET.SubElement(dataIndex, "dataIndexEntries")
        return dataIndexEntries


    def dataIndexEntry(self,dataIndexEntries,filePath, dataType , dataId,dataName ,dataBattleScribeVersion, dataRevision):
        dataIndexEntry = ET.SubElement(dataIndexEntries, "dataIndexEntry")
        dataIndexEntry.attrib["filePath"] = filePath
        dataIndexEntry.attrib["dataType"] = dataType
        dataIndexEntry.attrib["dataId"] = dataId
        dataIndexEntry.attrib["dataName"] = dataName
        dataIndexEntry.attrib["dataBattleScribeVersion"] = dataBattleScribeVersion
        dataIndexEntry.attrib["dataRevision"] = dataRevision
        #return dataIndex

di = DataIndexer()

dataIndex = di.indexInitializer()
di.indexRepositoryUrls(dataIndex)
dataIndexEntries = di.indexDataIndexEntries(dataIndex)
di.dataIndexEntry(dataIndexEntries, filePath="Warhammer_40.000_8th_Edition.gst" ,dataType="gamesystem" ,dataId="49b6-bc6f-0390-1e40", dataName="Warhammer 40,000 8th Edition-BR", dataBattleScribeVersion="2.01", dataRevision="74")
di.dataIndexEntry(dataIndexEntries, filePath="Warhammer_40.000_8th_Edition.gst" ,dataType="gamesystem" ,dataId="49b6-bc6f-0390-1e40", dataName="Warhammer 40,000 8th Edition-BR", dataBattleScribeVersion="2.01", dataRevision="74")
di.dataIndexEntry(dataIndexEntries, filePath="Warhammer_40.000_8th_Edition.gst" ,dataType="gamesystem" ,dataId="49b6-bc6f-0390-1e40", dataName="Warhammer 40,000 8th Edition-BR", dataBattleScribeVersion="2.01", dataRevision="74")
di.dataIndexEntry(dataIndexEntries, filePath="Warhammer_40.000_8th_Edition.gst" ,dataType="gamesystem" ,dataId="49b6-bc6f-0390-1e40", dataName="Warhammer 40,000 8th Edition-BR", dataBattleScribeVersion="2.01", dataRevision="74")

tree =   prettify(dataIndex)
with open("index.xml",'w') as xmlfile:
    xmlfile.write(tree)


"""dataIndexEntries = ET.SubElement(dataIndex, "dataIndexEntries")
dataIndexEntries.attrib["filePath"]="Warhammer_40.000_8th_Edition.gst"
dataIndexEntries.attrib["dataType"]="gamesystem"
dataIndexEntries.attrib["dataId"]="49b6-bc6f-0390-1e40"
dataIndexEntries.attrib["dataName"]="Warhammer 40,000 8th Edition-BR"
dataIndexEntries.attrib["dataBattleScribeVersion"]="2.01"
dataIndexEntries.attrib["dataRevision"]="74"""