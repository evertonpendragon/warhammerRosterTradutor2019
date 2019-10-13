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
import zlib


originPath = "./wh40k-master/"
destPath = "./wh40k_PTBR-master/"


print '\n\n\n\n',  'Compactando arquivo'
os.chdir(destPath)
destCatFiles = os.listdir('.')
destCatFiles = filter(lambda x: x[-1] != 'z', destCatFiles)
for f in destCatFiles:
    print f
    compression = zip.ZIP_DEFLATED
    with zip.ZipFile(f+'z', mode='w') as zip_ref:
        zip_ref.write( f, compress_type=compression)
        zip_ref.close()
    os.remove(f)
