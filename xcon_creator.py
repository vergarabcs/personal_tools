import pyautogui as pag
from pag import click, hotkey
import re
import pyperclip
import csv
import json
import time
import os

class Config:
    KEY_NAME = 'IncidentPathDeterminationLabelKey'
    LABEL_NAME = 'IncidentPathDeterminationLabel'
    class FILE_NAME:
        MOBILITY_SCRIPTS = 'I18nKeyValue - Mobility Scripts.tsv'
        LABELS = 'I18nKeyValue - Sheet1.tsv'

def clean(given):
    return given.replace('#', 'num')

def to_capital_snake(given:str):
    return given.replace(' ', '_').upper()

def create_key(given, prefix=''):
    # given = clean(given)
    if prefix:
        return f'{prefix}_{to_capital_snake(given)}'
    else:
        return to_capital_snake(given)

def xcon_inputs(key, string):
    time.sleep(0.2)
    click('xcon_add_script.png', memoize=True)
    time.sleep(0.2)
    click('xcon_script_key.png', memoize=True)
    pyperclip.copy(key)
    hotkey('command', 'v')
    pag.press('tab')
    pyperclip.copy(string)
    hotkey('command', 'v')
    pag.press('tab')
    pag.press('enter')
    pag.press('enter')


def parse_schemas():
    with open('./input/schemas.txt', "r") as f:
        schemas_txt = f.read()
        # # matches = re.findall('''.*value:.*['"](.*)['"]''', schemas_txt)
        # matches_label = re.findall('''.*label:.*['"](.*)['"]''', schemas_txt)
        # dedup_set = set()
        # # for match in matches:
        # #     dedup_set.add(match.strip())
        # print(len(list(matches_label)))
        # for match in matches_label:
        #     dedup_set.add(match.strip())
        # dedup_list = list(dedup_set)
        # dedup_list.sort()
        # for x in dedup_list:
        #     if(not x.strip()):
        #         continue
        #     print(create_key(x))
        #     # print(x)
        # return dedup_list
        matches = re.findall('''searchconfig: \[(.*?)\]''', schemas_txt, re.DOTALL)
        for match in matches:
            print(match)
            break

def translate_list(string_list, language_code):
    print(string_list)
    import boto3

    session = boto3.Session(profile_name='asurion-mobility-ac-nonprod.dev')

    translate = session.client(
        service_name='translate', 
        region_name='us-east-1', 
        use_ssl=True,
    )

    with open(f'./output/{language_code}_table.tsv', 'w') as fd:
        writer = csv.writer(fd, delimiter='\t')
        for [key, string, _] in string_list:
            print(key, string)
            result = translate.translate_text(
                Text=string, 
                SourceLanguageCode="en",
                TargetLanguageCode=language_code
            )
            writer.writerow([
                key,
                string,
                result.get('TranslatedText')
            ])

def translate(lang_code):
    with open(f'./input/I18nKeyValue - Sheet1.tsv', 'r') as fd:
        reader = csv.reader(fd, delimiter='\t')
        reader = filter(lambda x: x[2] != 'Uploaded', reader)
        translate_list(list(reader), lang_code)

def main():
    hotkey('command', 'tab')
    string_list = parse_schemas()
    string_list = filter(lambda x: len(x) > 0, string_list)
    translate_list(string_list, 'ja')
    for x in string_list:
        print(x)

def read_translation_table_and_add_to_xcon(lang, file_name):
    col_i = 1 if lang == 'en' else 3
    pag.PAUSE = 0.2
    hotkey('command', 'tab')

    os.system(f"mv '/Users/billcarlo.vergara/Downloads/{file_name}' '/Users/billcarlo.vergara/Projects/oms_automation/input/xcon_upload_input.tsv'")
    with open(f'./input/xcon_upload_input.tsv', 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        for idx, row in enumerate(reader):
            if(idx == 0): continue
            if(row[2] in ['Uploaded', 'WorkbasketUploaded']): continue
            print(row)
            xcon_inputs(row[0], row[col_i])
    hotkey('command', 'tab')

def upload_existing():
    temp_dict = dict()
    with open('./input/from_xcon.json', 'r') as f:
        data = json.load(f)
        for lang in data:
            for key in data[lang]:
                if not key in temp_dict:
                    temp_dict[key] = dict()
                temp_dict[key][lang] = data[lang][key]
    with open('./output/from_xcon.tsv', 'w') as f:
        writer = csv.writer(f, delimiter='\t')
        for key in temp_dict:
            if(not 'en' in temp_dict[key]):
                print(f'{key}: ', temp_dict[key]['ja'])
                print()
                continue

            writer.writerow([
                key,
                temp_dict[key]['en'],
                'Uploaded'
            ])

def dynJsonToTsv(name):
    with open(f'./input/{name}.json', 'r') as f:
        with open(f'./output/{name}.tsv', 'w', encoding="utf-8") as fo:
            writer = csv.writer(fo, delimiter='\t')
            data = json.load(f)
            for key in data['M']:
                value = data['M'][key]['S']
                writer.writerow([key, value])
            

# dynJsonToTsv("Scripts-rtl-en")
# translate('ja')
read_translation_table_and_add_to_xcon('ja', Config.FILE_NAME.LABELS)
# upload_existing()
# parse_schemas()