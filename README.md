# grevys-zebra-individual-identification
Coming soon
## Dataset
The data is a combination of the test and validation dataset from [smalst](https://github.com/silviazuffi/smalst). In total it includes 4 unqiue images of 37 indivdiual Grevy's Zebras taken at The Great Grevy's Rally 2018. Please download both datasets and then place all the images into a single folder.
Coming soon
## Pipeline Components & Architecture
* Animal Detection
* Species Classification
* Deep 3D Fitting
* Identification through Deep Metric Learning
## Setup
* Create the virtual environment - `python -m venv venv_zebra` 
* Activate the env - `source venv_zebra\bin\activate` 
* Add the required packages, then deactivate and reactivate the env - `pip install -r requirements.txt`
* run setup.sh to get the submodule repo's - `python setup.sh` 

## Models
Animal Detection requires The MegaDetector [model file](https://github.com/microsoft/CameraTraps/blob/main/megadetector.md#using-the-model). It will assume the model is downloaded to the "modules" folder. If a different model is used change the name in the script, as the current script will assume you downloaded MDv4.1, there are minor changes required to run the more recent model files (such as MDv5a and MDv5b) which are described [here](https://github.com/microsoft/CameraTraps/blob/main/megadetector.md#using-the-model)

`SpeciesClassification/classify_images.py ` contains urls to the classification model and taxonomy utalised. These can be downloaded and the urls replaced with paths to their location.


## Citation
Coming soon
## Acknowledgements
Coming soon
## Next steps
* Compare MDv5a and MDv5b against MDv4.1 performance and implement changes to be able to alternative versions
* Change virtual vnvironment to anaconda environment
