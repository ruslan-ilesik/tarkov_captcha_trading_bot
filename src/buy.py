from __main__ import screen
from constants import *
import my_sleep as time 
from captcha import *

import pyautogui

def buy_first():
    pyautogui.click(BUY_BTN[0]*screen.width+random_offset(), BUY_BTN[1]*screen.height+random_offset())
    time.sleep(0.1)
    pyautogui.press("y")
    time.sleep(0.3)
    solve_captcha()
    pyautogui.click(PRESS_BUY_FAIL[0]*screen.width+random_offset(), PRESS_BUY_FAIL[1]*screen.height+random_offset())
    time.actions_cnt +=1
    time.sleep(0.5)