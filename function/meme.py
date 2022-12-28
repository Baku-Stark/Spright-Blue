import os
import random

def memeSelect(serverFolder):
    if serverFolder == "servertcg":
        dir_images = os.listdir(r"img_memes\servertcg")
        image_choice = random.choice(dir_images)
        return image_choice

    else:
        dir_images = os.listdir(r"img_memes\o_servers")
        image_choice = random.choice(dir_images)
        return image_choice