import pyautogui
import pyperclip

from __main__ import screen
from constants import *

import my_sleep as time

def clear():
    pyautogui.click(NAME_INPUT_POS[0]*screen.width+random_offset(), NAME_INPUT_POS[1]*screen.height+random_offset())
    pyautogui.hotkey('ctrl','a')
    time.sleep(0.1)
    pyautogui.press('backspace')
    time.sleep(0.1)

def put_text(string : str):
    pyautogui.click(NAME_INPUT_POS[0]*screen.width+random_offset(), NAME_INPUT_POS[1]*screen.height+random_offset())
    time.sleep(0.1)
    pyperclip.copy(string)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(3)

def select_first():
    pyautogui.click(FIRST_IN_SEARCH[0]*screen.width+random_offset(), FIRST_IN_SEARCH[1]*screen.height+random_offset())
    time.sleep(0.5)
    pyautogui.hotkey("f5")
    time.actions_cnt +=1
    time.sleep(0.5)