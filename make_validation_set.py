import os  
import shutil 
from os import path as Path
import glob
import random

image_folder_path = 'C://Users//AEZ//Documents//SDI//RoadCracks//CrackForest//Images//' #/ image_folder
mask_folder_path = 'C://Users//AEZ//Documents//SDI//RoadCracks//CrackForest//Masks//' #/ mask_folder
image_folder_val = 'C://Users//AEZ//Documents//SDI//RoadCracks//CrackForest//Images_val//' 
mask_folder_val = 'C://Users//AEZ//Documents//SDI//RoadCracks//CrackForest//Masks_val//'



def move_image_mask_to_val_folder(val_set):
    for item in val_set:
        image_name = item.replace('png', 'jpg')
        #move image
        shutil.move(image_folder_path + image_name, image_folder_val + image_name)
        shutil.move(mask_folder_path + item, mask_folder_val + item)  
  


def make_val_set():
    image_names = []
    mask_names = []
    for file in glob.glob(image_folder_path+'*.jpg'):
        fileName = os.path.basename(file)
        image_names.append(fileName)
        mask_name = fileName.replace('jpg','png')
        mask_path = mask_folder_path +'//'+ mask_name
        
        #check if mask exists
        if Path.exists(mask_path):
            mask_names.append(mask_name)
    
    # shuflle the both image_names and mask_names
    random.shuffle(mask_names)
    # get only 10% of the samples
    val_set = mask_names[:int(len(mask_names)-( len(mask_names) * 0.9))]
    
    move_image_mask_to_val_folder(val_set)


make_val_set()
