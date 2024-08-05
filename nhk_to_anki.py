from pag import click, hotkey, waitForImage, waitForImageToVanish
import time
import pyautogui as pag
import pyperclip
from bs4 import BeautifulSoup
import csv
import os
from nhk_scraper import get_articles
from os import system


class State:
    should_repeat = True

TAG = "NHK_WEB_EASY"

def isCompleteTags(text):
    # </explanation> is removed and instead will wait for generating indicator to vanish
    tags = ["<explanation>", "<translation>", "</translation>"]
    return all(map(lambda tag: tag in text, tags))

def split_translation_explanation(cgpt_response):
    soup = BeautifulSoup(cgpt_response,'html.parser')
    try:
        if(not isCompleteTags(cgpt_response)):
            raise "Incomplete"
        translation = soup.find('translation').text.strip()
        explanation = soup.find('explanation').text.strip()
        State.should_repeat = False
    except Exception as e:
        system('say exception')
        print(e)
        pag.hotkey("command", "tab", interval=0.2)
        except_command = input('Error encountered. Enter any character to continue.')
        if(except_command == "exit"):
            raise e
        time.sleep(1)
        pag.hotkey("command", "tab", interval=0.2)
        return (None, None)

    return (translation, explanation)

def waitForResponseFinished():
    hasVanished = waitForImageToVanish('inprogress_indicator.png', 30, 120)
    if(not hasVanished):
        system('say exception')
        pag.hotkey("command", "tab", interval=0.2)
        except_command = input('Error encountered. Enter any character to continue.')
        if(except_command == "exit"):
            raise 'End it'
        time.sleep(1)
        pag.hotkey("command", "tab", interval=0.2)

def start_loop(writer):
    for idx, sentence_list in enumerate(get_articles(0)):
        context = None
        for sentence in sentence_list:
            pag.hotkey("shift", "escape", interval=0.2)
            pyperclip.copy(f'{sentence}\n\nPlease make sure to include the <translation>, <explanation> and their closing tags.')
            pag.hotkey("command", "v")
            pag.press("enter")
            waitForResponseFinished()

            while(State.should_repeat):
                (x, y) = pag.size()
                pag.moveTo(x/2, y/2)
                pag.scroll(-20)
                pag.hotkey("command", "shift", "c")
                cgpt_response = pyperclip.paste()
                (translation, explanation) = split_translation_explanation(cgpt_response)
            State.should_repeat = True
            if(not context):
                context = translation
            
            writer.writerow([
                sentence, # id
                sentence, # japanese
                sentence, # reading
                context, # context
                translation, # english,
                explanation, # explanation,
                '', # screenshot
                '', # audio_sentence
                '', # audio_english
                '', # video
                TAG,
            ])
        
        print('article', idx)
        pag.hotkey("command", "shift", "o", interval=0.2)

def transferPastHeadlines():
    dedupe_set = set()
    with open('./input/finishedHeadlines2.tsv', 'r') as destFile:
        destReader = csv.reader(destFile)
        for idx, row in enumerate(list(destReader)):
            dedupe_set.add(row[0])
            print(row[0])
    with open('./input/currentHeadlines.tsv', 'r') as sourceF, open('./input/finishedHeadlines2.tsv', 'a+') as destF:
        reader = csv.reader(sourceF)
        writer = csv.writer(destF)        
        for idx, row in enumerate(list(reader)):
            if(row[0] in dedupe_set):
                continue
            writer.writerow(row)

def main():
    # try:
    transferPastHeadlines()
    try:
        pag.hotkey("command", "tab", interval=0.2)
        with open('nhk_out.tsv', 'w') as fd:
            writer = csv.writer(fd, delimiter='\t')
            start_loop(writer)
    except Exception as e:
        print(e)
    move_to_public()
    pag.hotkey("command", "tab", interval=0.2)
    system('say scraping finished')

def move_to_public():
    os.system('cp ./nhk_out.tsv ~/Public/nhk_out.tsv' )

main()