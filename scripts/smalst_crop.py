#!/usr/bin/env python3
import argparse
import os
import sys
import PIL
from pathlib import Path
from tokenize import String
sys.path.insert(1, '..')

from CameraTraps.visualization import visualization_utils as viz_utils

parser = argparse.ArgumentParser(
	description=" Crop of SMALST output in IIZ pipeline",
	formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument(
	"--input",
	type=Path,
	help="Input directory of texture images"
)
parser.add_argument(
	"--output",
	type=Path,
	help="Output directory for cropped textures"
)
parser.add_argument(
	"--extension",
	type=String,
    default=".png",
	help=""
)
def cropping_texture(data, output_path, view):
	image = viz_utils.load_image(data)
	filename = view +"_"+data.split("/")[-1]
	out_file = os.path.join(output_path,filename)
	crop_l = [{"conf":0.9, "bbox":[0.21,0.36,0.19,0.27]}] 
	crop_r = [{"conf":0.9, "bbox":[0.61,0.70,0.19,0.27]}]  
	if view == "left" :
		croppedImages = viz_utils.crop_image(crop_r, image, confidence_threshold=0.7)
		rotatedImage = croppedImages[0].rotate(180).transpose(PIL.Image.FLIP_LEFT_RIGHT)
		rotatedImage.save(out_file)
	else:
		croppedImages = viz_utils.crop_image(crop_l, image, confidence_threshold=0.7)
		croppedImages[0].save(out_file)

def main(args):

    for f in os.listdir(args.input):
        ext = os.path.splitext(f)[1]
        if ext.lower() != args.extension:
            continue
        filename = f.split("/")[0] 
        if "tex" not in filename:
            continue
        filename = filename.split("tex_")[1]
        data = os.path.join(args.input,f)
        cropping_texture(data,args.output,"left")
        cropping_texture(data,args.output,"right")

if __name__ == "__main__":
	main(parser.parse_args())