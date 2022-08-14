#!/bin/sh

source /user/work/gh18931/diss/grevys-zebra-individual-identification/venv_zebra/bin/activate
# Assumes images are of Grevy zebras and already cropped.

export PYTHONPATH="$PYTHONPATH:$(realpath modules/CameraTraps):$(realpath modules/ai4utils)"
export OUTPUT_DIR = # put here a directory for training/test data once split
# This will create the test/train folder and class subfolders within and split the dataset
# Currently the split is 50:50 due to dataset size so change that split value to what is expected
python training_loader.py --preprocess  --data=$OUTPUT_DIR/unprocessed_data --output=$OUTPUT_DIR
#
python augmentation.py  --colour_jitter  --pos_rotate   --neg_rotate --translation --vertical_trans  --horizontal_trans --multiple=3 --input_path=$OUTPUT_DIR/train_unprocessed

cd..

python -m smalst.smal_eval --img_path=$OUTPUT_DIR/test_unprocessed/ --bgval=0 --num_train_epoch=130 -use_annotations=False --segm_eval=False  --save_input=True   --name="smal_net" --out_path=$OUTPUT_DIR/test_unprocessed 
python -m smalst.smal_eval --img_path=$OUTPUT_DIR/train_unprocessed/ --bgval=0 --num_train_epoch=130 -use_annotations=False --segm_eval=False  --save_input=True   --name="smal_net" --out_path=$OUTPUT_DIR/train_unprocessed 

python training_loader.py --data=$OUTPUT_DIR/test_unprocessed --csv_data=$OUTPUT_DIR/labels-id.csv --img_ext=".png" 
python training_loader.py --data=$OUTPUT_DIR/train_unprocessed --csv_data=$OUTPUT_DIR/labels-id.csv --img_ext=".png" 
 
cd ..
cd MetricLearningIdentification

python train.py --out_path=output --eval_freq=1 --folds_file=splits$OUTPUT_DIR/folds.json  --dataset=Zebra --n_neighbours=1 --batch_size=8 --triplet_lambda=0.0001 --learning_rate=0.1 --num_epochs=2010