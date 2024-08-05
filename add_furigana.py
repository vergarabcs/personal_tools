import pyautogui
from pag import click
import time
def main():
    ORIGINAL = pyautogui.PAUSE
    pyautogui.PAUSE = 0.2
    pyautogui.hotkey('command', 'tab', interval=0.2)
    (x, y) = (None, None)
    for i in range(45):
        if not x:
            (x, y) = click('add_furigana.png')
        else:
            pyautogui.click(x, y)
        time.sleep(0.5)
        pyautogui.hotkey('command', 'n')
    pyautogui.PAUSE = ORIGINAL

main()