#!/usr/bin/env python3
import argparse

from pathlib import Path
import json
import sys
import os
sys.path.insert(1, '..')
from AnimalDetection.CameraTraps.visualization import visualization_utils as viz_utils

output_path = ""


parser = argparse.ArgumentParser(
    description=" Animal Detection Cropping through using MegaDetector",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument(
    "--crop",
    action="store_true",
    help="Will images be cropped"
)
parser.add_argument(
    "--input_filepath",
    type=Path,
    help = "Directory of images"
)
parser.add_argument(
    "--output_filepath",
    type=Path,
    help = "Output directory for cropped images"
)
parser.add_argument(
    "--threshold",
    type=int,
    default = 0.7,
    help = "Confidence threshold"
)

def get_detections(inputpath, threshold):
    imagedict = {}
    detectiondict = {}
    with open(inputpath) as detection_json:
        data = json.load(detection_json)
        for img in data['images']:
            try:
                filename = img['file']
                imagedict[filename] = img['detections']
                detectiondict[filename] = []
                for detection in img['detections']:
                    if detection['conf'] > threshold and detection['category'] == "1":
                        detectiondict[filename].append(detection)
            except:
                pass
    return imagedict, detectiondict

def process_image(args): 
    images , detections = get_detections(args.input_filepath, args.threshold)

    for img in images:
        
        image = viz_utils.load_image(img)
        im_filename = img.split("/")[-1][:-4]
        print(im_filename)
        if args.crop:
            cropped_im = viz_utils.crop_image(detections[img],image,confidence_threshold= args.threshold)
            for i in range(len(cropped_im)):
                output_name = im_filename+str(i) + ".jpg"
                cropped_im[i].save(args.output_filepath / output_name )
        else:
            viz_utils.render_detection_bounding_boxes(detections[img],image,confidence_threshold= args.threshold)
            output_name = im_filename+".jpg"
            image.save( args.output_filepath / output_name )

    
        

def main(args):
    if not os.path.exists(args.output_filepath):
        os.makedirs(args.output_filepath)
    process_image(args)


if __name__ == "__main__":
    main(parser.parse_args())