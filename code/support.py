from settings import *
import os
from os import walk

def import_image(*path,format="png",alpha=True):
    full_path=get_absolute_path(*path)+f'.{format}'
    return pygame.image.load(full_path).convert_alpha() if alpha  else pygame.image.load(full_path).convert()


def import_folder(*path):
    frames=[]
    for folder_path, _,file_names in walk(get_absolute_path(*path)):
        for file in sorted(file_names,key=lambda name:int(name.strip(".")[0])):
            full_path=get_absolute_path(folder_path,file)
            image=pygame.image.load(full_path).convert_alpha()
            frames.append(image)
    return frames


def audio_importer(*path):
    audio_dict={}
    for folder_path,_,file_names in walk(get_absolute_path(*path)):
        for file in file_names:
            full_path=get_absolute_path(folder_path,file)
            audio_dict[file.split(".")[0]]=pygame.mixer.Sound(full_path)
    return audio_dict

def get_image(sheet, frame_x, frame_y, width=PlAYER_TILE_SIZE,height=PlAYER_TILE_SIZE,start_number=0,end_number=1):
    """Cut a part of the image from the sprite sheet."""
    frames=[]
    for  i in range(end_number):
        image = pygame.Surface((width, height), pygame.SRCALPHA)  # Create a transparent surface
        image.blit(sheet, (0, 0), ((frame_x+i) * width, frame_y * height, width, height))  # Blit from sheet
        image=pygame.transform.scale(image,(280,280))
        frames.append(image)
    return frames