#!/usr/bin/env python3
import argparse
import os
from pathlib import Path

parser = argparse.ArgumentParser(
	description="Folder creation script",
	formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument(
	"--path",
	type=Path,
	help="Where data is stored to go through the pipeline"
)
def main(args):
    isExist = os.path.exists(args.path)
    if isExist:# Check the directory given exists
        
        # Create all the subdirectories
        md_dir = os.path.join(args.path,"MegaDetector_output")
        os.makedirs(md_dir,exist_ok=True)
        sc_dir = os.path.join(args.path,"SpeciesClassification_output")
        os.makedirs(sc_dir,exist_ok=True)
        smalst_dir = os.path.join(args.path,"SMALST_output")
        os.makedirs(smalst_dir,exist_ok=True)
        dml_dir = os.path.join(args.path,"DML_input")
        os.makedirs(dml_dir,exist_ok=True)
    else:# if not then error
        print("Path given is not a value directory")
        exit(1)
    

if __name__ == "__main__":
	main(parser.parse_args())