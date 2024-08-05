
import pyautogui
import time
import os
from AppKit import NSScreen


SCALE_FACTOR = NSScreen.screens()[0].backingScaleFactor()

class Memo:
    def __init__(self) -> None:
        self.cache = dict()

memo = Memo()

def click(filename, memoize=False):
    cached_coords = memo.cache.get(filename)
    (x, y) = cached_coords if cached_coords else (None, None)
    while(True):
        try:
            if(not memoize or not x):
                x, y = pyautogui.locateCenterOnScreen(f"./images/{filename}", confidence=0.80)
                memo.cache[filename] = (x, y)
            pyautogui.moveTo(x, y)
            time.sleep(1)
            pyautogui.click(x/SCALE_FACTOR, y/SCALE_FACTOR)
            return (x/SCALE_FACTOR, y/SCALE_FACTOR)
        except pyautogui.ImageNotFoundException:
            time.sleep(1)

def waitForImage(filename, minWaitSeconds=30, maxWaitSeconds=60):
    startTime = time.time()
    time.sleep(minWaitSeconds)
    while(True):
        try:
            pyautogui.locateCenterOnScreen(f"./images/{filename}", confidence=0.80)
            return None
        except pyautogui.ImageNotFoundException:
            currTime = time.time()
            if(currTime - startTime > maxWaitSeconds):
                return None
            time.sleep(1)

def waitForImageToVanish(filename, minWaitSeconds=30, maxWaitSeconds=90):
    startTime = time.time()
    time.sleep(minWaitSeconds)
    print('waiting. . .')
    while(True):
        try:
            (x, y) = pyautogui.locateCenterOnScreen(f"./images/{filename}", confidence=0.99)
            os.system(f'image found at "{x} and {y}"')
            pyautogui.moveTo(x, y)
            print(x, y)
            currTime = time.time()
            if(currTime - startTime > maxWaitSeconds):
                return False
            time.sleep(1)
        except pyautogui.ImageNotFoundException:
            return True

def hotkey(*args, **kwargs):
    pyautogui.hotkey(*args, **kwargs, interval=0.2)