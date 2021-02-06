import cv2
from PIL import Image
import colors
import os.path
from os import path



def drawBoundingBox(img_name, x_min, y_max, class_name):

    lbl_dir = r'C:\Users\AEZ\Documents\SDI\RoadCracks\Data\LungLesion\Labels'
    img_dir = r'C:\Users\AEZ\Documents\SDI\RoadCracks\Data\LungLesion\Images'
    
    img_path = os.path.join(img_dir, img_name + '.jpg')
    lbl_path = os.path.join(lbl_dir, img_name + '.png')

    img = path.exists(img_path)
    lbl = path.exists(lbl_path)
    
    if img and lbl:
        img = cv2.imread(img_path)
        lbl = cv2.imread(lbl_path) 
    
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    lbl_rgb = cv2.cvtColor(lbl, cv2.COLOR_BGR2RGB)

    # Start coordinate, here (5, 5) 
    # represents the top left corner of rectangle 
    start_point = (x_min, x_min) 
    # Ending coordinate, here (220, 220) 
    # represents the bottom right corner of rectangle 
    end_point = (y_max, y_max) 
    # Blue color in BGR 
    #color = (255, 0, 0) 
    color = colors.colors_dict[class_name]
    # Line thickness of 2 px 
    thickness = 2  
    # Using cv2.rectangle() method 
    # Draw a rectangle with blue line borders of thickness of 2 px 
    img = cv2.rectangle(img_rgb, start_point, end_point, color, thickness) 
    img = Image.fromarray(img)
    img.show()

    lbl = cv2.rectangle(lbl_rgb, start_point, end_point, color, thickness) 
    lbl = Image.fromarray(lbl)
    lbl.show()
    return img, lbl

drawBoundingBox('Lung_Dx-A0001#04-04-2007-Chest-07990#3.000000-5mm-41315#1-17', 220, 380, 'A')