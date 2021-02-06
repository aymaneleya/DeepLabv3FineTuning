import numpy as np
import matplotlib as mlp
import PIL
from PIL import Image
import tqdm
import glob, os
import cv2



class ISIC_Data_Preparation:
    def __init__(self):
        self.img_dir = "C://Users//AEZ//Documents//SDI//RoadCracks//Data//ungLesion//"#"C://Users//AEZ//Documents//SDI//RoadCracks//samples//Images//"
        self.mask_dir = "C://Users//AEZ//Documents//SDI//RoadCracks//Data//LungLesion//Segmentation_label//"#"C://Users//AEZ//Documents//SDI//RoadCracks//samples//Masks//"
        self.img_renamed_dir = "C://Users//AEZ//Documents//SDI//RoadCracks//samples_all//Images_renamed//"
        self.mask_renamed_dir = "C://Users//AEZ//Documents//SDI//RoadCracks//samples_all//Masks_renamed//"
        self.SPACE = 35
        self.UNIT_SCALE = True


    def convert_mask_to_black_white(self, single_mask_path):
        org_mask = cv2.imread(single_mask_path)
        gery_mask = cv2.cvtColor(org_mask, cv2.COLOR_BGR2GRAY)
        (thresh, blackAndWhiteImage) = cv2.threshold(gery_mask, 0, 255, cv2.THRESH_BINARY)
        blackAndWhiteImage = np.expand_dims(blackAndWhiteImage, axis=1)
        blackAndWhiteImage = blackAndWhiteImage.reshape(512, 512, 1)
        return blackAndWhiteImage

    def save_new_mask_imag(self, name):
        org_mask = cv2.imread(single_mask_path)
        gery_mask = cv2.cvtColor(org_mask, cv2.COLOR_BGR2GRAY)
        (thresh, blackAndWhiteImage) = cv2.threshold(gery_mask, 0, 255, cv2.THRESH_BINARY)
        return blackAndWhiteImage
 

    def get_masks_and_image(self):
        counter = 1
        for root, dirs, files in os.walk(self.img_dir):
            for file in files:
                img_name = file
                mask_name = file.replace('jpg','png')

                img_path = self.img_dir + img_name
                mask_path = self.mask_dir + mask_name
                
                im = os.path.isfile(self.img_dir + img_name)
                lb = os.path.isfile(self.mask_dir + mask_name)
                
                if im and lb:
                    org_img = cv2.imread(img_path) 
                    cv2.imwrite(os.path.join(self.img_renamed_dir , str(counter) + '.jpg') ,org_img)
                    
                    #resize the label to (1,512,512)
                    org_mask = self.convert_mask_to_black_white(mask_path)
                    cv2.imwrite(os.path.join(self.mask_renamed_dir , str(counter) + '.png') ,org_mask)
                    #save image with new name
                    counter = counter + 1



myclass = ISIC_Data_Preparation()
myclass.get_masks_and_image()
