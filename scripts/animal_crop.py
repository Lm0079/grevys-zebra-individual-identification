#!/usr/bin/env python3
from AnimalDetection.CameraTraps.visualization import visualization_utils as viz_utils
import argparse
import os
from pathlib import Path
from PIL import Image
import json
import sys
sys.path.insert(1, '..')


# python animal_crop.py --md_filepath=/user/work/gh18931/diss/giraffe_identification/great_dataset_detection_output.json --input_filepath=/user/work/gh18931/diss/gzgc.coco/images/train2020 --output_filepath=/user/work/gh18931/diss/giraffe_identification/output/megadetector/

parser = argparse.ArgumentParser(
	description="Animal Detection Cropping through using MegaDetector with filtering and paddings",
	formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument(
	"--md_filepath",
	type=Path,
	help="Filepath for MegaDetector output"
)
parser.add_argument(
	"--input_filepath",
	type=Path,
	help="Directory of images"
)
parser.add_argument(
	"--output_filepath",
	type=Path,
	default='/user/work/gh18931/diss/giraffe_identification/output/megadetector',
	help="Output directory for cropped images"
)
parser.add_argument(
	"--threshold",
	type=int,
	default=0.83,
	help="Confidence threshold"
)

'''
Reads the MegaDetector output and stores in dictionary to be parsed later on.
Only stores boundingboxes of animals that have a confidence level over a threshold value
'''
def predicted_bboxes(inputpath, threshold):
	megaDetectorBboxes = []
	with open(inputpath) as json_file:
		data = json.load(json_file)
		for p in data['images']:
			file_name = p['file']
			bbox = {"file": file_name}

			for detection in p['detections']:
				if detection['conf'] > threshold and detection['category'] == "1":
					if "bbox" in bbox:
						bbox["bbox"].append(detection['bbox'])
					else:
						bbox["bbox"] = [detection['bbox']]
			if "bbox" in bbox:
				bbox["bbox"] = convert_to_float(bbox["bbox"])
				megaDetectorBboxes.append(bbox)
	return megaDetectorBboxes


'''
Checks if there is overlap between bounding boxes
'''

def is_overlap(bboxes):
	overlap = False
	for j in bboxes:
		for k in bboxes:
			if j != k:
				if bb_intersection_over_union(k, j) > 0:
					overlap = True
	return overlap


'''
Checks to see if a bounding box is within another any bounding boxes
'''

def is_contained(j, bboxes):
	contained = False
	for k in bboxes:
		if j != k:
			contained = contained or contained_check(k, j)
	return contained


'''
Checks if a bounding box is within another bounding box
'''

def contained_check(bb_1, bb_2):
	outer, inner = bb_1, bb_2
	return inner[0] >= outer[0] and inner[1] >= outer[1] and inner[0]+inner[2] <= outer[0]+outer[2] and inner[1]+inner[3] <= outer[1]+outer[3]


'''
Crops image based on MD detections that have not been filtered out
'''
def crop_image(bbox, image_name, image_id, output_path, threshold):
	image = viz_utils.load_image(image_name)
	# Threshold was already checked in predicted_bboxes function so arbitrary conf added.
	image_det = {"bbox": bbox, "conf": 0.99}
	croppedImages = viz_utils.crop_image(
		[image_det], image, confidence_threshold=threshold)

	alteredFileName = image_name.split("/")[-1]
	alteredFileName = alteredFileName[:-4]
	output_name = alteredFileName + "-" + str(image_id)+".jpg"
	croppedImages[0].save(output_path/output_name)


'''
'''

def output_bounding_images(predictedBB, args):
	for predicted in predictedBB:
		name = predicted["file"]
		image_id = 0
		width, height = Image.open(name).size
		bboxes = predicted["bbox"]

		if len(bboxes) == 0:  # There are no bounding boxes
			pass
		elif len(bboxes) == 1:  # A single bounding box in the image
			bbox = pad_normalised_bbox(bboxes[0], width, height)
			crop_image(bbox, name, image_id,
					   args.output_filepath, args.threshold)
			image_id += 1
		else:  # Multiple bounding boxes

			if is_overlap(bboxes):
				not_contained_bboxes = []
				for bbox in bboxes:
					if not is_contained(bbox, bboxes):
						not_contained_bboxes.append(bbox)
				for j in not_contained_bboxes:

					low_IOU = False
					for k in not_contained_bboxes:
						if j != k:
							if bb_intersection_over_union(k, j) > 0.3:
								
								j_area = calculate_area(j)
								k_area = calculate_area(k)
								if k_area <= j_area:
									not_contained_bboxes.remove(k)
								else:
									not_contained_bboxes.remove(j)
					if j in not_contained_bboxes:
						bbox = pad_normalised_bbox(j, width, height)

						crop_image(bbox, name, image_id,
								   args.output_filepath, args.threshold)
						image_id += 1
						low_IOU = True
			else:
				for j in bboxes:
					bbox = pad_normalised_bbox(j, width, height)
					crop_image(bbox, name, image_id,
							   args.output_filepath, args.threshold)
					image_id += 1
# ---- helper functions---------------


def unnormalise_image(bbox, width, height):
	return [bbox[0]*width, bbox[1] * height, bbox[2] * width, bbox[3]*height]


def normalise_image(bbox, width, height):
	return [bbox[0]/width, bbox[1] / height, bbox[2] / width, bbox[3]/height]


def calculate_area(bbox):
	return bbox[2] * bbox[3]


def pad_normalised_bbox(bbox, width, height):
	padding = 100
	bbox = unnormalise_image(bbox, width, height)
	bbox = [max(bbox[0]-padding, 0), max(bbox[1]-padding, 0),
			min(bbox[2]+2*padding, width), min(bbox[3]+2*padding, height)]
	bbox = normalise_image(bbox, width, height)

	return bbox


def convert_to_float(input):

	return [[float(l) for l in ls]for ls in input]

def coco_to_pascal(c_arr):
	return [c_arr[0],c_arr[1],c_arr[0]+c_arr[2],c_arr[1]+c_arr[3]]
	
def bb_intersection_over_union(pred, truth):
	pred = coco_to_pascal(pred)
	truth = coco_to_pascal(truth)
	xA = max(pred[0], truth[0])
	yA = max(pred[1], truth[1])
	xB = min(pred[2], truth[2])
	yB = min(pred[3], truth[3])
	interArea = max(0, xB - xA ) * max(0, yB - yA )

	predArea = (pred[2] - pred[0] ) * (pred[3] - pred[1] )
	truthArea = (truth[2] - truth[0] ) * (truth[3] - truth[1] )
	##TODO add a check for divide by 0 case
	iou = interArea / float(predArea + truthArea - interArea)

	return iou


def main(args):
	if not os.path.exists(args.output_filepath):
		os.makedirs(args.output_filepath)
	predicted = predicted_bboxes(args.input_filepath, args.threshold)
	output_bounding_images(predicted, args)


if __name__ == "__main__":
	main(parser.parse_args())
