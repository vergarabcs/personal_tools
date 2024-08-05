import pyautogui
import time
from pag import click
OMS_URL = "https://teams.microsoft.com/_#/apps/10c4e309-aebc-44d5-8fec-24f6d681f4a0/sections/86e93592-ea51-42bd-b150-5ff8f6176ab5"
DAYS_AGO = 5           
def select_10pm():
    for i in range(4):
        pyautogui.press("up")
    pyautogui.press("Enter")

def one_day_add(day_delta):
    click("add.png")
    
    click("date.png")
    pyautogui.hotkey("shift", "tab")

    #move cursor to today:
    for i in range(15):
        pyautogui.press("right")
    
    # move cursor to today minus day_delta
    for i in range(day_delta):
        pyautogui.press("left")
    time.sleep(1)
    pyautogui.press("Enter")
    
    click("ot_classification.png")
    time.sleep(1)
    pyautogui.press("Enter")

    #from
    click("from_to_dropdown.png")
    select_10pm()

    #to
    click("from_to_dropdown.png")
    pyautogui.press("up")
    pyautogui.press("Enter")

    click("check.png")

def main():
    # pyautogui.hotkey("command", "space") does not work for some reason
    with pyautogui.hold('command'):
        pyautogui.press("space")
    pyautogui.write("Google Chrome")
    pyautogui.press("enter")
    pyautogui.hotkey("command", "n")
    pyautogui.hotkey("command", "l")
    pyautogui.typewrite(OMS_URL)
    pyautogui.press("enter")

    click("new_request.png")
    
    for i in range(DAYS_AGO, DAYS_AGO-5, -1):
        one_day_add(i)
    # click("check2.png")
    # click("check3.png")

main()