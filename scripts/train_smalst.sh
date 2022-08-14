#!/bin/sh
# run the same command as in the trainng scripts in smalst repo
cd ..
python -m smalst.experiments.smal_shape --zebra_dir='/user/work/gh18931/diss/datasets/zebra_training_set'  --num_epochs=210 --num_images=15000  --save_training_imgs=False --save_epoch_freq=5  --name=smal_net
