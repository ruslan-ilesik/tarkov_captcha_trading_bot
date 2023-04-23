from __main__ import screen
from constants import *

import pyautogui
import my_sleep as time

def change_to(which : str): #FLEA_MARKET, TRADERS 
    pyautogui.click(BOTTOM_TABS[which][0]*screen.width+random_offset(), BOTTOM_TABS[which][1]*screen.height+random_offset())
    time.sleep(0.2)

def go_to_trader(which : str): 
    change_to("TRADERS")
    pyautogui.click(TRADERS[which][0]*screen.width+random_offset(), TRADERS[which][1]*screen.height+random_offset())
    time.sleep(0.2)