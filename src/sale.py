from __main__ import screen
from constants import *

import pyautogui
import my_sleep as time
from captcha import *

def make_sale():
    time.sleep(0.7)
    pyautogui.click(SELL_TAB[0]*screen.width+random_offset(), SELL_TAB[1]*screen.height+random_offset())
    pyautogui.keyDown('ctrl')
    time.sleep(0.4)
    pyautogui.click(FIRST_SLOT_IN_INVENTORY[0]*screen.width+random_offset(), FIRST_SLOT_IN_INVENTORY[1]*screen.height+random_offset())
    pyautogui.keyUp('ctrl')
    time.sleep(0.2)
    pyautogui.click(MAKE_SELL[0]*screen.width+random_offset(), MAKE_SELL[1]*screen.height+random_offset())
    time.actions_cnt +=1
    time.sleep(0.2)
    solve_captcha()