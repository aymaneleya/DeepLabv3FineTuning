# this file reads the path of the annotation of each image, and stores the image name, min_x, max_x, min_y, max_y in csv file
import pandas as pd
from bs4 import BeautifulSoup
import os.path
from os import path
import cv2
import numpy as np


def read__annotation_from_xml(path):
    xml = BeautifulSoup(open(path), 'xml')
    x_min = xml.find('xmin').getText()
    y_min = xml.find('ymin').getText()
    x_max = xml.find('xmax').getText()
    y_max = xml.find('ymax').getText()
    ann = {'x_min' : x_min, 'y_min' : y_min, 'x_max' : x_max, 'y_max' : y_max }
    return ann

def get_image_label(image_name):
    
    img_name = image_name.replace('.dcm','')
    
    lbl_dir = r'C:\Users\AEZ\Documents\SDI\RoadCracks\Data\LungLesion\Labels'
    img_dir = r'C:\Users\AEZ\Documents\SDI\RoadCracks\Data\LungLesion\Images'
    
    img_path = os.path.join(img_dir, img_name + '.jpg')
    lbl_path = os.path.join(lbl_dir, img_name + '.png')

    img = path.exists(img_path)
    lbl = path.exists(lbl_path)
    
    if img and lbl:
        img = cv2.imread(img_path)
        lbl = cv2.imread(lbl_path) 
        img_rgb = img#cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        lbl_rgb = lbl#cv2.cvtColor(lbl, cv2.COLOR_BGR2RGB)
        return img_rgb, lbl_rgb
    
    return None, None

def get_class_sub_dir(image_name):
    
    if 'Lung_Dx-A' in image_name:
        return 'A'
    elif 'Lung_Dx-B' in image_name:
        return 'B'
    elif 'Lung_Dx-E' in image_name:
        return 'E'
    elif 'Lung_Dx-G' in image_name:
        return 'G'
    else:
        return  'Unknown'

def convert_mask_to_black_white(lbl):
    gery_mask = cv2.cvtColor(lbl, cv2.COLOR_BGR2GRAY)
    (thresh, blackAndWhiteImage) = cv2.threshold(gery_mask, 0, 255, cv2.THRESH_BINARY)
    blackAndWhiteImage = np.expand_dims(blackAndWhiteImage, axis=1)
    blackAndWhiteImage = blackAndWhiteImage.reshape(512, 512, 1)
    return blackAndWhiteImage
# making data frame from csv file 
data = pd.read_csv(r"C:\Users\AEZ\Documents\SDI\RoadCracks\Data\LungLesion\\imagePathAndAnnotationPath.csv") 

# sorting dataframe 
data.sort_values('ImageDirName', inplace = True) 
df = data  

# Lung_Dx-A0001,1-13.dcm,Lung_Dx-A0001#04-04-2007-Chest-07990#2.000000-5mm-40805#1-13.dcm,D:\\MedicalImages\\Lung-PET-CT-Dx\\Lung_Dx-A0001\\04-04-2007-Chest-07990\\2.000000-5mm-40805\\1-13.dcm,C:\\Annotation\\A0001\\1.3.6.1.4.1.14519.5.2.1.6655.2359.184131899543495374569818432657.xml

# we need the customer to make sure unique names 
counter = 1
d = []
lbl_save_dir = r'C:\Users\AEZ\Documents\SDI\RoadCracks\Data\LungLesion\Data_Renamed\Labels'
lbl_g_s_save_dir = r'C:\Users\AEZ\Documents\SDI\RoadCracks\Data\LungLesion\Data_Renamed\Labels_grey_scale'
img_save_dir = r'C:\Users\AEZ\Documents\SDI\RoadCracks\Data\LungLesion\Data_Renamed\Images'
#for each row in the df
for index, row in df.iterrows():
    image_full_name = row['ImageFullName']
    img, lbl = get_image_label(image_full_name)

    ann_path = row['AnnotationPath']
    ann = read__annotation_from_xml(ann_path)
    
    if img is not None and lbl is not None and len(ann) == 4:
        #Lung_Dx-A0001,1-13.dcm,
        img_dir_name = row['ImageDirName'].replace('Lung_Dx-','')
        img_name = str(counter) + '_' + img_dir_name + '_' + row['ImageName'].replace('dcm','jpg')
        lbl_name = str(counter) + '_' + img_dir_name + '_' + row['ImageName'].replace('dcm','png')
        
        d.append((img_name, lbl_name, ann['x_min'], ann['y_min'], ann['x_max'], ann['y_max']))
        
        class_sub_dir = get_class_sub_dir(row['ImageDirName'])
        #save image
        cv2.imwrite(os.path.join(img_save_dir , class_sub_dir, img_name), img)
        #save label RGB
        cv2.imwrite(os.path.join(lbl_save_dir , class_sub_dir, lbl_name), lbl)
        #save label grey scale
        cv2.imwrite(os.path.join(lbl_g_s_save_dir , class_sub_dir, lbl_name), convert_mask_to_black_white(lbl))
        counter = counter + 1
    #print(row['ImageName'], row['ImageDirName'])
        new_df = pd.DataFrame(d, columns=('img_name', 'lbl_name', 'x_min', 'y_min', 'x_max', 'y_max'))
    if index % 100 == 0:
        print('Processing indecies: ' + str(index) +'. Number of processed images: '+ str(counter))
new_df.to_csv(r'C:\Users\AEZ\Documents\SDI\RoadCracks\Data\LungLesion\Data_Renamed\annotation.csv', index=False)
