import cv2
import numpy as np
import pytesseract
import sys
sys.setrecursionlimit(100000)
from mss import mss
import pytesseract
pytesseract.pytesseract.tesseract_cmd = "./tesseract/tesseract.exe"

from __main__  import screen, settings
from constants import *


def __recursion_remove(pos,to_analize):
    stack = [pos]
    while stack:
        i, j = stack.pop()
        if i < 0 or i >= len(to_analize) or j < 0 or j >= len(to_analize[0]):
            continue
        if to_analize[i][j].tolist() != [0, 0, 0, 255]:
            to_analize[i][j] = [0, 0, 0, 255]
            stack.append([i, j+1])
            stack.append([i+1, j])
            stack.append([i-1, j])
            stack.append([i, j-1])


def get_smallest_price():
    cords = {'top': 0,'left': 0,'width':int(screen.width * PRICE_END[0]), 'height':int(screen.height * PRICE_END[1])}
    with mss() as sct :
        img = np.array(sct.grab(cords))
        crop_img = img[ int(screen.height * PRICE_START[1])::, int(screen.width * PRICE_START[0])::]
        to_analize = np.copy(crop_img)
        #remove curency
        pos = [0,0]
        (thresh, to_analize) = cv2.threshold(to_analize, 127, 255, cv2.THRESH_BINARY)
        for y in reversed (range(len(to_analize))):
            for x in reversed (range(len(to_analize[y]))):
                if to_analize[y][x].tolist() != [0,0,0,255]:
                    pos = [y,x]
                    break
            if pos != [0,0]:
                break
        __recursion_remove(pos,to_analize)
        


        text = pytesseract.image_to_string(to_analize, config='--psm 8 -c tessedit_char_whitelist=0123456789')
        try:
            return (int(text),crop_img)
        except:
            return  (99999999999,crop_img)


def is_rubles(img) -> bool :
    for i in img:
        for j in i:
            if j.tolist() == EURO_COLOR or j.tolist() == DOLLAR_COLOR:
                return False
    return True

def is_currency(img, currency) -> bool :
    for i in img:
        for j in i:
            if j.tolist() == EURO_COLOR:
                return ("EUR" == currency) 
            if j.tolist() == DOLLAR_COLOR:
                return ("USD" == currency) 
    return ("RUB" == currency)

def get_currency(img) -> str :
    for i in img:
        for j in i:
            if j.tolist() == EURO_COLOR:
                return "EUR"
            if j.tolist() == DOLLAR_COLOR:
                return "USD"
    return "RUB"


def convert_to_rubles(amount, currency):
    if (currency == "USD"):
        return amount * settings.getint("CURRENCY","usd")
    if (currency == "EUR"):
        return amount* settings.getint("CURRENCY","eur")
    
    return amount
