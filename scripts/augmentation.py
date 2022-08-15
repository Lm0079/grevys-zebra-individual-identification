#!/usr/bin/env python3
import argparse
import numpy as np
from pathlib import Path
import cv2
import os
import random
parser = argparse.ArgumentParser(
    description="Data Augmentation for DML training",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)

parser.add_argument(
    "--input_path",
    type=Path,
    help=""
)
parser.add_argument(
    "--output_path",
    type=Path,
    help=""
)
parser.add_argument(
    "--flip",
    action="store_true",
    help="  "
)
parser.add_argument(
    "--colour_jitter",
    action="store_true",
    help="  "
)
parser.add_argument(
    "--pos_rotate",
    action="store_true",
    help="  "
)
parser.add_argument(
    "--neg_rotate",
    action="store_true",
    help="  "
)
parser.add_argument(
    "--translation",
    action="store_true",
    help="  "
)
parser.add_argument(
    "--vertical_trans",
    action="store_true",
    help="  "
)
parser.add_argument(
    "--horizontal_trans",
    action="store_true",
    help="  "
)
parser.add_argument(
    "--adding_contrast",
    action="store_true",
    help="  "
)
parser.add_argument(
    "--multiple",
    type=int, default=1,
    help=" "
)

# Augmentation through altering image brightness
def brightjitter(img,value):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    if value >= 0:
        lim = 255 - value
        v[v > lim] = 255
        v[v <= lim] += value
    else:
        lim = np.absolute(value)
        v[v < lim] = 0
        v[v >= lim] -= np.absolute(value)

    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img

# Augmentation through altering image saturation
def saturationjitter(img,value):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    if value >= 0:
        lim = 255 - value
        s[s > lim] = 255
        s[s <= lim] += value
    else:
        lim = np.absolute(value)
        s[s < lim] = 0
        s[s >= lim] -= np.absolute(value)

    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img

# Augmentation through altering image contrast
def contrastjitter(img,contrast):
    brightness = 10
    dummy = np.int16(img)
    dummy = dummy * (contrast/127+1) - contrast + brightness
    dummy = np.clip(dummy, 0, 255)
    img = np.uint8(dummy)
    return img

# Performs C,S,B colour augmentations
def colorjitter(img, cj_type="b"):
    '''
    ### Different Color Jitter ###
    img: image
    cj_type: {b: brightness, s: saturation, c: constast}
    '''
    if cj_type == "b":
        value = np.random.choice(np.array([-50, -40, -30, 30, 40, 50, 45, -45]))
        img = brightjitter(img,value)
    
    elif cj_type == "s":
        value = np.random.choice(np.array([-50, -40, -30, 30, 40, 50, 45, -45]))
        img = saturationjitter(img,value)
    
    elif cj_type == "c":
        value = random.randint(40, 100)
        img = contrastjitter(img, value)

    return img ,value
    
#
def flip(img):
    img = cv2.flip(img, 1)
    return img

#
def vert_translation(img):
    value = np.random.choice([0.1,-0.1,0.05,-0.05,0.2,-0.2])
    height, width = img.shape[:2]
    ty =  height * value
    translation_matrix = np.array([
    [1, 0, 0],
    [0, 1, ty]
    ], dtype=np.float32)
    translated_image = cv2.warpAffine(src=img, M=translation_matrix, dsize=(width, height))
    
    return translated_image, value

#
def translation(img):
    value = np.random.choice([0.05,-0.05,0.1,-0.1])
    height, width = img.shape[:2]
    tx ,ty = width * value, height * value
    translation_matrix = np.array([
    [1, 0, tx],
    [0, 1, ty]
    ], dtype=np.float32)
    translated_image = cv2.warpAffine(src=img, M=translation_matrix, dsize=(width, height))
    return translated_image,value

#
def hor_translation(img):
    value = np.random.choice([0.1,-0.1,0.05,-0.05,0.2,-0.2])
    height, width = img.shape[:2]
    tx = width * value
    translation_matrix = np.array([
    [1, 0, tx],
    [0, 1, 0]
    ], dtype=np.float32)
    translated_image = cv2.warpAffine(src=img, M=translation_matrix, dsize=(width, height))
    return translated_image, value

#
def pos_rotation(img):
    value = np.random.choice(np.arange(4,18,2))
    height, width = img.shape[:2]
    center = (width/2, height/2)
    rotate_matrix = cv2.getRotationMatrix2D(center=center, angle=value, scale=1)
    rotated_image = cv2.warpAffine(src=img, M=rotate_matrix, dsize=(width, height))
    return rotated_image, value

#
def neg_rotation(img):
    height, width = img.shape[:2]
    value = np.random.choice(np.arange(4,18,2))
    center = (width/2, height/2)
    rotate_matrix = cv2.getRotationMatrix2D(center=center, angle=-value, scale=1)
    rotated_image = cv2.warpAffine(src=img, M=rotate_matrix, dsize=(width, height))
    return rotated_image,value

#
def output_img(path, img):
    print(path)
    cv2.imwrite(path, img)

#
def output_colour_jitter(img,type,output,filename,ext):
    complete = False
    while not complete:
        jittered_img, value =  colorjitter(img,type)
        jittered_file = output+"/"+filename +"_"+type+str(value)+ ext
        if not os.path.exists(jittered_file):
            complete = True
            print(jittered_file)
            output_img(jittered_file,jittered_img)

#
def output_rotation(img,output,filename,ext,pos):
    complete = False
    while not complete:
        if pos:
            rotated_img,value = pos_rotation(img)
            rotated_file = str(output)+"/"+filename +"_pos_rotation" + str(value)+ ext
        else:
            rotated_img,value = neg_rotation(img)
            rotated_file = str(output)+"/"+filename +"_neg_rotation"+ str(value)+ ext
            
        if not os.path.exists(rotated_file):
            complete = True
            output_img(rotated_file,rotated_img)

#
def output_translation(img,output,filename,ext,vert):
    complete = False
    while not complete:
        if vert:
            trans_img,value =vert_translation(img)    
            translated_file = str(output)+"/"+filename +"_vert_translation" + str(value)+ ext
        else:
            trans_img,value = hor_translation(img)
            translated_file = str(output)+"/"+filename +"_hori_translation" + str(value)+ ext
            
        if not os.path.exists(translated_file):
            complete = True
            output_img(translated_file,trans_img)

#
def output_shift(img, output, filename, ext):
    complete = False
    while not complete:
        translated_img,value = translation(img)
        translated_file = str(output)+"/"+filename +"_translation"+ str(value)+ ext
        if not os.path.exists(translated_file):
            complete = True
            output_img(translated_file,translated_img)

def main(args):
    
    np.random.seed(0)
    image_ext = ".jpg"
    for f in os.listdir(args.input_path):
        ext = os.path.splitext(f)[1]
        if ext.lower() != image_ext:
            continue
        original_image= cv2.imread( str(args.input_path)+"/"+f)
        filename = f.split("/")[0].split(image_ext)[0]
        if args.flip:
            flipped_file = str(args.input_path)+"/"+filename +"_flipped"+ image_ext
            flipped_img = flip(original_image)
            output_img(flipped_file,flipped_img)
        if args.colour_jitter:
            for i in range(args.multiple):
                output_colour_jitter(original_image,"b",str(args.input_path),filename,image_ext)
                output_colour_jitter(original_image,"s",str(args.input_path),filename,image_ext)
                output_colour_jitter(original_image,"c",str(args.input_path),filename,image_ext)
        if args.pos_rotate:
            for i in range(args.multiple):
                output_rotation(original_image,args.input_path,filename, image_ext,True)
        if args.neg_rotate:
            for i in range(args.multiple):
                output_rotation(original_image,args.input_path,filename, image_ext,False)
        if args.translation:
            for i in range(args.multiple):
                output_shift(original_image,args.input_path,filename,image_ext)
        if args.vertical_trans:
            for i in range(args.multiple):
                output_translation(original_image,args.input_path, filename, image_ext, True)
        if args.horizontal_trans:
            for i in range(args.multiple):
                output_translation(original_image,args.input_path, filename, image_ext, False)
            

if __name__ == "__main__":
    main(parser.parse_args())