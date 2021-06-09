import fnmatch
import os
import zipfile
import os.path
import re
import sys
import json
import shutil

with open('settings.json', encoding="utf8") as settigs_file:
    settings = json.load(settigs_file)
    first_path = settings['rules']['firstPath']    # 'DocFlow/Правила конвертации DF2ERPBF/'
    second_path = settings['rules']['secondPath']  # 'ERP BF/Правила конвертации ERPBF2DF/'
    first_zip = settings['rules']['firstZip']      # 'Правила обмена DF2ERPBF.zip'
    second_zip = settings['rules']['secondZip']    # 'Правила обмена ERPBF2DF.zip'
    synckCorrAndExch = settings['rules']['synckCorrAndExch'] # 'флаг синхронизации файлов CorrespondentExchangeRules.xml и CorrespondentExchangeRules.xml'

includes = ['*.xml']
includes = r'|'.join([fnmatch.translate(x) for x in includes])


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        files = [os.path.join(path, f) for f in files]
        files = [f for f in files if re.match(includes, f)]
        for file in files:
            file_path = os.path.join(path, file)
            ziph.write(file_path, os.path.basename(file_path))


def create_zip(path, name):
    zipf = zipfile.ZipFile(name, 'w', zipfile.ZIP_DEFLATED)
    zipdir(path, zipf)
    zipf.close()


if __name__ == '__main__':
    # Строим полные пути от папки запуска
    start_path = os.path.dirname(sys.argv[0])
    first_path = os.path.join(start_path, first_path)
    first_zip = os.path.join(start_path, first_zip)

    second_path = os.path.join(start_path, second_path)
    second_zip = os.path.join(start_path, second_zip)

    # Синхронизируем правила выгрузки с правилами корреспондирующей базы
    # ExchangeRules.xml CorrespondentExchangeRules.xml
    if synckCorrAndExch == True:
        shutil.copy(os.path.join(first_path, r'ExchangeRules.xml'), os.path.join(second_path, r'CorrespondentExchangeRules.xml'))
        shutil.copy(os.path.join(second_path, r'ExchangeRules.xml'), os.path.join(first_path, r'CorrespondentExchangeRules.xml'))

    create_zip(first_path, first_zip)
    create_zip(second_path, second_zip)
