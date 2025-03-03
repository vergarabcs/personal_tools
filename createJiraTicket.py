from pag import hotkey
import pyautogui
import time
import os

class Config:
    TITLE = '''Brew Triggered Create New Client in App Config'''
    DESCRIPTION = '''Brew Triggered Create New Client in App Config'''
    DUE_DATE = '4/March/25'
    SPRINT = 'S04'

def pressXtimes(key, count):        
    for i in range(count):
        pyautogui.press(key)

def main():
    # title = input("Title?")
    print("Title:")
    print(Config.TITLE)
    print()
    time.sleep(1)
    hotkey('command', 'tab')
    pyautogui.typewrite("c")
    time.sleep(4)

    # Title
    pressXtimes("tab", 5)
    pyautogui.typewrite(Config.TITLE)
    
    # Scrum Team
    pressXtimes('tab', 1)
    pyautogui.typewrite('Horizon - Alpha')
    
    # Description
    pressXtimes('tab', 2)
    pyautogui.typewrite(Config.TITLE)

    # Assignee
    pressXtimes('tab', 6)
    pyautogui.press('enter')
    
    # Due Date
    pressXtimes('tab', 3)
    pyautogui.typewrite(Config.DUE_DATE)

    # QA DROP OFF
    pressXtimes('tab', 2)
    pyautogui.typewrite(Config.DUE_DATE)

    # Sprint
    pressXtimes('tab', 3)
    pyautogui.typewrite(Config.SPRINT)
    time.sleep(1)
    os.system("say 'finished'")



main()