import os.path
import requests
import json
import cv2
from tqdm import tqdm
from PIL import Image

path = "./game_info/image_cash/"

f = open("./game_info/items.json",encoding="utf-8")
original = json.loads(f.read())
f.close()
name_id_dict = {}

print("Loading info for captcha...")
for item in tqdm(original):
    name_id_dict[item["name"]] = item["id"]
    name_id_dict[item["shortName"]] = item["id"]




def get_image(name):
    id = name_id_dict[name]
    img_path = path+id+".png"
    if os.path.isfile(img_path):
        img = cv2.imread(img_path) 
        return img
    im = Image.open(requests.get("https://assets.tarkov.dev/"+id+"-8x.webp", stream=True).raw)
    im.save(img_path)
    img = cv2.imread(img_path) 
    return img
