import fnmatch
import os
import zipfile
import os.path
import re
import sys
import json
import shutil
import subprocess

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

    with open('settings.json', encoding="utf8") as settigs_file:
        settings = json.load(settigs_file)
        first_path = settings['rules']['firstPath']    # 'DocFlow/Правила конвертации DF2ERPBF/'
        second_path = settings['rules']['secondPath']  # 'ERP BF/Правила конвертации ERPBF2DF/'
        first_zip = settings['rules']['firstZip']      # 'Правила обмена DF2ERPBF.zip'
        second_zip = settings['rules']['secondZip']    # 'Правила обмена ERPBF2DF.zip'

        first_base_server = settings['test']['firstBaseServer']
        second_base_server = settings['test']['secondBaseServer']
        first_base_name = settings['test']['firstBaseName']
        second_base_name = settings['test']['secondBaseName']
        exchange_name = settings['test']['exchangeName']
        set_rules_processor = settings['test']['setRulesProcessorPath']

    includes = ['*.xml']
    includes = r'|'.join([fnmatch.translate(x) for x in includes])

    # Строим полные пути от папки запуска
    start_path = os.path.dirname(sys.argv[0])
    first_path = os.path.join(start_path, first_path)
    first_zip = os.path.join(start_path, first_zip)

    second_path = os.path.join(start_path, second_path)
    second_zip = os.path.join(start_path, second_zip)

    # Синхронизируем правила выгрузки с правилами корреспондирующей базы
    shutil.copy(os.path.join(first_path, r'ExchangeRules.xml'), os.path.join(second_path, r'CorrespondentExchangeRules.xml'))
    shutil.copy(os.path.join(second_path, r'ExchangeRules.xml'), os.path.join(first_path, r'CorrespondentExchangeRules.xml'))

    create_zip(first_path, first_zip)
    create_zip(second_path, second_zip)
 
    set_rules_command = '"C:\\Program Files\\1cv8\\8.3.18.1483\\bin\\1cv8.exe" ENTERPRISE \
        /S"{}/{}" \
        /DisableStartUpMessages \
        /DisableStartupDialogs \
        /Execute"{}" \
        /C"ИмяПланаОбмена={};ФайлПравил={}"'.replace("  ","")

    subprocess.check_call(set_rules_command.format(first_base_server,first_base_name,set_rules_processor,exchange_name,first_zip), shell=True)
    subprocess.check_call(set_rules_command.format(second_base_server,second_base_name,set_rules_processor,exchange_name,second_zip), shell=True)
    pass