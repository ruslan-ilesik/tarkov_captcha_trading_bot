from mss import mss
import numpy as np
from PIL import Image
import cv2
import pyautogui
from get_image_by_name import *
from Levenshtein import distance
from __main__ import screen, settings
from find_price import *
import my_sleep as time
from tqdm import tqdm

from constants import *
from change_tabs import *

def closest_string(s, strings):
    min_distance = float('inf')
    closest_string = None
    for string in strings:
        dist = distance(s, string)
        if dist < min_distance:
            min_distance = dist
            closest_string = string
    return closest_string


def solve_captcha():
    is_found = False
    square = []
    cords = {'top': 0,'left': 0,'width':int(screen.width), 'height':int(screen.height)}
    find = False
    with mss() as sct :
        img = np.array(sct.grab(cords))
        for y in range(len(img)):
            for x in range(len(img[y])):
                if img[y][x].tolist()  == CAPTCHA_COLOR:
                    is_found = True
                    print("Captcha detected."+("Solwing..." if settings.getboolean("GLOBAL_SETTINGS","solve_captcha") else "Freezing..."))
                    if not settings.getboolean("GLOBAL_SETTINGS","solve_captcha"):
                        input("Press enter to continue running bot")
                        return
                
                    #Get captcha square
                    square.append([x,y])
                    while img[y][x].tolist()  == CAPTCHA_COLOR:
                        x+=1
                    x-=1
                    while img[y][x].tolist()  == CAPTCHA_COLOR:
                        y+=1
                    y-=1
                    square.append([x,y])
                    print(square)
                    find = True
                    break
            if find: 
                break
        if not find:
            return
        
        match_size = screen.width/30

        captcha_img = img[square[0][1]:square[1][1], square[0][0]:square[1][0]]
        (thresh, captcha_img) = cv2.threshold(captcha_img, 127, 255, cv2.THRESH_BINARY)
        text = pytesseract.image_to_string(captcha_img)
        text = text.split("You must choose all:")[-1]
        text = closest_string(text,name_id_dict.keys())
        print("Captcha asked to find: ",text)
        print("Searching...")
        match_image = get_image(text)

        match_image = cv2.resize(match_image, (int(match_size * (len(match_image[0])/512)),int(match_size * (len(match_image)/512))) )
        match_image = cv2.cvtColor(match_image, cv2.COLOR_RGBA2RGB)
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
        w, h = match_image.shape[:-1]

        res = cv2.matchTemplate(img, match_image, cv2.TM_CCOEFF_NORMED)
        threshold = 0.9
        tryes = 1
        places_to_click = []
        while len(places_to_click) == 0:
            print("Trying", tryes, " time")
            threshold -=0.1
            tryes +=1
            loc = np.where(res >= threshold)
            for pt in zip(*loc[::-1]):  # Switch columns and rows
                cv2.rectangle(img, pt, (pt[0] + h, pt[1] + w), (0, 0, 255), 2)

                add = True
                for i in places_to_click:
                    if abs(i[0] - pt[0]) < match_size-1 and abs(i[1] - pt[1]) < match_size:
                        add = False
                
                if add:
                    places_to_click.append(pt)

            for i in tqdm(places_to_click):
                pyautogui.click(i[0]+match_size/2, i[1]+match_size/2)
                time.sleep(0.3)

    #find confirm btn
    x = square[0][0]-7
    y = square[0][1]
    while img[y][x].tolist()  == CAPTCHA_BG_COLOR:
        y+=1
    pos = [square[0][0] + ((square[1][0] - square[0][0])/2), y-match_size/2]
    pyautogui.click(pos[0],pos[1])
    time.sleep(2.5)
    solve_captcha()
    print("Solved, continuing...")
    change_to("FLEA_MARKET")
    if not is_found:
        return
