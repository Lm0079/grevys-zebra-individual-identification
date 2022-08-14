# grevys-zebra-individual-identification
Deep learning technqiues for species detection, 3D model fitting, and metric learning are combined to form a novel pipeline for the individual identification of Grevy's zebras from photographs by utalising their unique coat patterns like a fingerprint. 

This achieved an indentifcation accuracy of 56.8% on the SMALST dataset. This study is far to small to estimate the full perfromance pontential or for comparisions against polished tools, but acts as a proof-of-concept and possible groundwork for further steps.

## Dataset
The data is a combination of the test and validation dataset from [smalst](https://github.com/silviazuffi/smalst). In total it includes 4 unqiue images of 37 indivdiual Grevy's Zebras taken at The Great Grevy's Rally 2018. Please download both datasets and then place all the images into a single folder.

*Note- Each side of the animal has a distinctive pattern so must be classified separately.*

## Pipeline Components & Architecture
*TODO - Add image*

* Animal Detection -  [MegaDetector](https://github.com/microsoft/CameraTraps/blob/main/megadetector.md) can detect animals, people, and vehicles in camera trap images. In this pipeline MDv4.1 is used which is a F-RCNN ensemble of Inception and ResNet streams to detect object instances of a generic ‘animal’ class. Any detections with a confidence level below 0.83 (determined via AUC optimisation) is filtered out.
* Species Classification - [SpeciesClassifiction](https://github.com/Lm0079/SpeciesClassification) is a pre-trained species classification model by Microsoft’s AI for Earth team to perform species disambiguation. The model fuses combines Inception and ResNext outputs to confirm a species, in this case that the animal present is a Grevy's zebra.
presence against any other species
* Deep 3D Fitting - *to be added soon*
* Identification through Deep Metric Learning - *to be added soon*


**To be updated/continued soon**
## Setup
* Create the virtual environment - `python -m venv venv_zebra` 
* Activate the env - `source venv_zebra\bin\activate` 
* Add the required packages, then deactivate and reactivate the env - `pip install -r requirements.txt`
*Note- Depending on the system it is running on, the versions of the packages may need to be modified.*
* run setup.sh to get the submodule repo's - `python setup.sh` 

## Training

[Contact me](mariastennett@hotmail.co.uk) if further help is needed.
## Models
Animal Detection requires The MegaDetector [model file](https://github.com/microsoft/CameraTraps/blob/main/megadetector.md#using-the-model). It will assume the model is downloaded to the "models" folder. If a different model is used change the name in the script, as the current script will assume you downloaded MDv4.1, there are minor changes required to run the more recent model files (such as MDv5a and MDv5b) which are described [here](https://github.com/microsoft/CameraTraps/blob/main/megadetector.md#using-the-model)

`SpeciesClassification/classify_images.py ` contains urls to the classification model and taxonomy utalised. These can be downloaded and the urls replaced with paths to their location.

*deep 3D fitting model - to be added soon*

*deep metric learnng model - to be added soon*


## Citation
This work was submitted and presented at the Visual observation and analysis of Vertebrate And Insect Behaviour workshop at the International Conference on Pattern Recognition (ICPR 2022). If you do use this work as part of your research, please cite [Towards Individual Grevy's Zebra Identification via Deep 3D Fitting and Metric Learning](https://arxiv.org/abs/2206.02261).
```text
@inproceedings{mstennett2022visual,
      title={Towards Individual Grevy's Zebra Identification via Deep 3D Fitting and Metric Learning}, 
      author={Stennett, Maria and Rubenstein, Daniel and  Burghardt, Tilo},
      year={2022},
      month=Aug,
      month_numeric = {8},
      booktitle={IEEE/IAPR International Conference on Pattern Recognition Workshop on Visual Observation and Analysis of Vertebrate And Insect Behavior (VAIB) },

}
```
## Acknowledgements
We appreciate publications by GGR/SMALST, WCS, MegaDetector, AI4Earth, and Andrew/Lagunes. Thanks to T Berger-Wolf, C Stewart, and J Parham.
This work was carried out using the computational facilities of the [Advanced Computing
Research Centre, University of Bristol](http://www.bris.ac.uk/acrc/)

## Next steps
* Compare MDv5a and MDv5b against MDv4.1 performance and implement changes to be able to alternative versions
* Change virtual vnvironment to anaconda environment
