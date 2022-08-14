#!/usr/bin/env python3
import argparse

from pathlib import Path
import csv
import sys
import os
import PIL
from sklearn.model_selection import train_test_split
 
sys.path.insert(1, '..')
from CameraTraps.visualization import visualization_utils as viz_utils


parser = argparse.ArgumentParser(
	description=" Training data reformatting",
	formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument(
	"--preprocess",
	action="store_true",
	help=" "
)
parser.add_argument(
	"--no_SMALST",
	action="store_true",
	help=" "
)
parser.add_argument(
	"--ablation_crop",
	action="store_true",
	help=" "
)
parser.add_argument(
	"--output",
	type=Path,
	help=""
)
parser.add_argument(
	"--data",
	type=Path,
	help=""
)
parser.add_argument(
	"--csv_data",
	type=Path,
	help=""
)

parser.add_argument(
	"--img_ext",
	type=str,
	default=".jpg",
	help=""
)


# Writes the data to csv 
def write_csv(data, name,columns,output_path):
	output_file = str(output_path) + "/"+ name
	try:
		with open(output_file, 'w') as f:
			w = csv.DictWriter(f, fieldnames=columns) 
			w.writeheader()
			for d in data:
				w.writerow(d)  
	except IOError:
		print("I/O error")

# Loads CSV file of Individual IDs and classes
def load_class_dict_csv(file):
	class_names = {}
	try:
		with open(file, 'r') as f:
			w= csv.DictReader(f,delimiter=',')
			line_count = 0
			lines = list(w)[1:]
			for row in lines:
				
				class_names[row["animal_id"]] = row["class"]

	except IOError:
		print("I/O error")
	
	return class_names

# Split the data into train/test and saves into separate folders
def split(file,target,viewpoints,output_path):
	x_train,x_test,y_train,y_test= train_test_split(file,target,random_state=42, test_size=0.5, stratify=target)
	for data,label in zip(x_test,y_test):
		file_output_path = output_path + "/test_unprocessed/"+ data.split("/")[-1]
		image = viz_utils.load_image(data)
		image.save(file_output_path)
	
	for data,label in zip(x_train,y_train):
		if label == 1:
			file_output_path = output_path + "/train_unprocessed/"+ "misc"+data.split("/")[-1]
		else:
			file_output_path = output_path + "/train_unprocessed/"+ data.split("/")[-1]
		image = viz_utils.load_image(data)
		image.save(file_output_path)
		

# Get the animal id for a given class		
def get_class_id(classes,animal_id):
	for aClass in classes:
		if aClass["animal_id"] == animal_id:
			return aClass["class"]

# Get viewpoint from file name
def get_viewpoint(filepath):
	if "right" in filepath :
		return "right"
	else:
		return "left"

# Flip the viewpoint
def opposite_viewpoint(viewpoint):
	if viewpoint == "left":
		return "right"
	else:
		return "left"

# Checks if folder exists, if not then it creates it 
def check_and_make_folder(path):
	isExist = os.path.exists(path)
	if not isExist:
		os.makedirs(path)

# Checks and creates train and test directories
def make_class_dir(output_path, animal_class):
	class_path_train =str( output_path) + "/train/" + str(animal_class)
	class_path_test = str(output_path) + "/test/"+ str(animal_class)
	if not animal_class == "1":
		check_and_make_folder(class_path_test)
	check_and_make_folder(class_path_train)

# Get animal ID in filename
def get_animal_id(filename,img_viewpoint):
	animal_id = ""
	if "female" in filename:
		animal_id = filename.split("_female")[0] + "_" + img_viewpoint
	else:
		animal_id = filename.split("_male")[0] + "_" + img_viewpoint
	return animal_id

# Gets class and filename infomation  from data
def calculate_data_files(data_labels):	
	file,target= [],[]
	count_for_misc = 0
	for data in data_labels:
		if data["class"] == 2:
			count_for_misc += 1
	for data in data_labels:
		if  (data["class"] != 1 ) or (data["class"] == 1 and count_for_misc >0):

			file.append(data["filename"])
			target.append(data["class"])
			if data["class"] == 1:
				count_for_misc -= 1
	return target,file

# Crops the texture maps
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

# Gathers ID infomation from filenames and splits dataset into train/test
def preprocessing(args):
	animal_classes = [{"class":1,"animal_id":"misc"}]
	make_class_dir(args.output,str(1))
	data_labels = []
	viewpoints = {}
	# id 1 is misc class
	id = 2
	for  data_path in [args.data]:
		valid_images = args.img_ext
		for f in os.listdir(data_path):
			ext = os.path.splitext(f)[1]
			if ext.lower() != valid_images:
				continue
			filename = f.split("/")[0] 
			img_viewpoint = get_viewpoint(filename)
			animal_id = get_animal_id(filename,img_viewpoint)
			class_defined = False

			for label in animal_classes:
				if label["animal_id"] == animal_id:
					class_defined = True
			if not class_defined:
				animal_classes.append({"class":id,"animal_id":animal_id})
				id += 1
			animal_class = get_class_id(animal_classes,animal_id)
			make_class_dir(args.output,str(animal_class))
			
			image_path = str(data_path)+"/"+f
			data_labels.append({"filename":image_path,"class":animal_class})
			data_labels.append({"filename":image_path,"class":1})
			viewpoints[(image_path,animal_class)]= img_viewpoint
			viewpoints[(image_path,1)] = opposite_viewpoint(img_viewpoint)
	
		
	target, file = calculate_data_files(data_labels)
	assert(len(file)== len(target))

	split(file,target,viewpoints,str(args.output))
	write_csv(animal_classes,"labels-id.csv",["class","animal_id"],args.output)



def main(args):

	if args.preprocess:
		preprocessing(args)
	else:

		print("Processing begins")
		output_data_path = str(args.data)
		output_data_path = output_data_path.replace("_unprocessed","")
		
		classes = load_class_dict_csv(args.csv_data)
		for  data_path in [args.data]:
			valid_images = args.img_ext
			for f in os.listdir(data_path):
				
				ext = os.path.splitext(f)[1]
				if ext.lower() != valid_images:
					continue
				filename = f.split("/")[0] 

				if not args.no_SMALST and not args.ablation_crop:
					if "tex" not in filename :
						continue
					filename = filename.split("tex_")[1]

				if args.ablation_crop:
					if "cropped_" not in filename:
						continue
					filename = filename.split("cropped_")[1]
				else:
					if "cropped_"  in filename:
						continue

				for animal_c in classes:
					if animal_c.split("_")[0] in filename:
						file_class = classes[animal_c]

				img_viewpoint = get_viewpoint(filename)
				if "misc" in filename:
					file_class = 1
					img_viewpoint = opposite_viewpoint(img_viewpoint)

				class_path = output_data_path + "/"+ str(file_class) 
				data = str(data_path)+"/"+f

				if args.no_SMALST or args.ablation_crop:
					image = viz_utils.load_image(data)
					filename = img_viewpoint +"_"+data.split("/")[-1]
					out_file = os.path.join(class_path,filename)
					image.save(out_file)
				else:
					cropping_texture(data, class_path, img_viewpoint)

		


				
	

if __name__ == "__main__":
	main(parser.parse_args())