import configparser
import os
from io import StringIO



def parseConfigFile(path):
    fullConfig = StringIO()
    realConfig = open(path)
    fullConfig.write('[main]\n')
    fullConfig.write(realConfig.read())
    fullConfig.seek(0, os.SEEK_SET)

    config = configparser.ConfigParser(
        delimiters=(' '))
    config.read_file(fullConfig)
    confDict = {}
    confDict['cpu_limit'] = config.getint('main', 'cpu_limit')
    confDict['document_root'] = config.get('main', 'document_root')
    # confDict['host'] = config.get('main', 'host')
    # confDict['port'] = config.getint('main', 'port')
    confDict['host'] = '0.0.0.0'
    confDict['port'] = 80


    return confDict




# ab -n 100000 -c 100 http://localhost:80/httptest/wikipedia_russia.html
