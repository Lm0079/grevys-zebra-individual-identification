#!/usr/bin/env python3
import argparse
from pathlib import Path
import sys
import cv2
import os
import csv
sys.path.insert(1, '..')
parser = argparse.ArgumentParser(
	description=" Species Filtering Script",
	formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument(
	"--species_filepath",
	type=Path,
	help="Filepath for species classification output"
)
parser.add_argument(
	"--output_filepath",
	type=Path,
	help="Filepath for output"
)

target_name =  "grévy's zebra"

def main(args):

	with open(args.species_filepath) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for row in csv_reader:
			if row[3] == "0": # Only checks the highest probability prediction
				predicted_category = row[5]
				if target_name == predicted_category:
					file_path = row[1]
					image = cv2.imread(file_path)
					file_name = file_path.split("/")[-1]
					output_filepath = Path(args.output_filepath , file_name)
					cv2.imwrite(str(output_filepath),image)
		


					   

	
	

	

if __name__ == "__main__":
	main(parser.parse_args())