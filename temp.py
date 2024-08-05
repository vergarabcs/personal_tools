from pag import waitForImage
import pyautogui

def main():
    waitForImage('response_finished_indicator.png', 5, 6)
    pyautogui.hotkey("command", "tab", interval=0.2)

main()