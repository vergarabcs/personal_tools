from os import system
import hashlib
import pyautogui
import pyperclip
system(f'mkdir -p output_audio')
pyautogui.PAUSE = 0.1
def main():
    pyautogui.hotkey('command', 'tab', interval=0.2)
    for i in range(64):
        pyautogui.hotkey('command', 'a')
        pyautogui.hotkey('command', 'c')
        string = pyperclip.paste()
        file_name = f'siri-{hashlib.md5(string.encode()).hexdigest()}.mp4'
        system(f'say -o output_audio/{file_name} "{string}"')
        for i in range(2):
            pyautogui.press('tab')
        pyautogui.hotkey('command', 'a')
        pyautogui.typewrite(f'[sound:{file_name}]')
        pyautogui.hotkey('command', 'n')
        for i in range(2):
            pyautogui.hotkey('shift', 'tab')
main()