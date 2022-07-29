#!/bin/sh
# TODO: improve pipeline and fail cases 
# Pipeline script going through all the stages.

# Activate the environment
source setup.sh

# Set up environment variables
## Where is the data coming from
export DATAPATH=/user/work/gh18931/diss/dataset
## Species Classification Input
export IMAGES=$DATAPATH/MegaDetector_output
## Species Classification Output
export OUTPUT=$DATAPATH/SpeciesClassification_output/sc_output.csv
## DML Model path
export MODEL=/user/work/gh18931/diss/MetricLearningIdentification/output/output1/new_aug_3/fold_0/best_model_state.pkl

# Set up the folders for each step to output too.
python set_up_folder.py --path=$DATAPATH
cd ..
# MegaDetector
python CameraTraps/detection/run_tf_detector_batch.py models/md_v4.1.0.pb $DATAPATH  $DATAPATH/MegaDetector_output/md_output.json
# Crop images based on Mega Detector output
python scripts/animal_crop.py --md_filepath=$DATAPATH/MegaDetector_output/md_output.json --input_filepath=$DATAPATH --outout_filepath=$DATAPATH/MegaDetector_output
# Species Classification
python SpeciesClassification/classify_images.py 
# Retains images of Grevy's Zebras
python scripts/species_cut.py --species_filepath=$OUTPUT --output_filepath=$DATAPATH/SpeciesClassification_output
#
python -m smalst.smal_eval --img_path=$DATAPATH/SpeciesClassification_output/ --bgval=0 --num_train_epoch=130 -use_annotations=False --segm_eval=False   --save_input=True --img_ext='.jpg' --out_path=$DATAPATH/SMALST_output  --name="smal_net"
#
python scripts/smalst_crop.py --input=$DATAPATH/SMALST_output --output=$DATAPATH/DML_input
#
python MetricLearningIdentification/run.py --model_path=$MODEL --input=$DATAPATH/DML_input --train_embeddings=train_embeddings.npz --save_path=$DATAPATH --class_labels=labels-id.csv
#

