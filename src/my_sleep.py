import time 
import random
import keyboard
from __main__ import settings
from other import *
from tqdm import tqdm

actions_cnt = 0

@static_vars(last_time=time.time())
def actions_checker():
        global actions_cnt

        if (settings.getint("SLOW_DOWN","actions_limit") == 0 or settings.getint("SLOW_DOWN","period") == 0):
                actions_cnt = 0
                return
       
        if time.time() - actions_checker.last_time  > settings.getint("SLOW_DOWN","period"):
                actions_cnt = 0
                actions_checker.last_time = time.time()
                return
        
        if actions_cnt > settings.getint("SLOW_DOWN","actions_limit"):
                print("Actions limit has been reached. Waiting...")
                for i in tqdm(range(int(settings.getint("SLOW_DOWN","period") - time.time() + actions_checker.last_time) * 10)):
                        time.sleep(0.1)
                        if (keyboard.is_pressed('q')):
                                print("exiting loop")
                                exit()
                print("Continue...")
        



def sleep(timeout): 
    if (keyboard.is_pressed('q')):
            print("exiting loop")
            exit()
    actions_checker()
          
    time.sleep(timeout+random.uniform(0.0, 0.1))
    return