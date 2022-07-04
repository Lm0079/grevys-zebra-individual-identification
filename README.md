# grevys-zebra-individual-identification
Coming soon
## Dataset
Coming soon
## Models
Animal Detection requires The MegaDetector [model file](https://github.com/microsoft/CameraTraps/blob/main/megadetector.md#using-the-model). It will assume the model is downloaded to the "modules" folder. If a different model is used change the name in the script, as the current script will assume you downloaded MDv4.1, there are minor changes required to run the more recent model files (such as MDv5a and MDv5b) which are described [here](https://github.com/microsoft/CameraTraps/blob/main/megadetector.md#using-the-model)


## Pipeline Components & Architecture
* Animal Detection
* Species Classification
* Deep 3D Fitting
* Identification through Deep Metric Learning
## Setup
* Create the virtual environment `python -m venv venv_zebra` 

## Citation
Coming soon
## Acknowledgements
Coming soon
## Next steps
* Compare MDv5a and MDv5b against MDv4.1 performance and implement changes to be able to alternative versions
* Change virtual vnvironment to anaconda environment
