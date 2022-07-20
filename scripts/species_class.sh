#!/bin/sh
# Script that performs only species classification filtering on a directory of images
# It requires setting up some paths required by the SC model.
# This will have to be done differently when run on windows
cd ..
#source venv_zebra/bin/activate
export OUTPUT=/sc_output.csv
export IMAGES=/MegaDetector_output

python ./SpeciesClassification/classify_images.py 
python ./scripts/species_crop.py --species_filepath=/user/work/gh18931/diss/grevys-zebra-individual-identification/sc_output.csv --output_filepath=/user/work/gh18931/diss/grevys-zebra-individual-identification/SC_output
#deactivate