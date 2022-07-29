
# TODO: add step to activate env 
git submodule update --init --recusive 
git submodule foreach git pull

# this is forcing cameratrap main code into the python import search path
export PYTHONPATH="$PYTHONPATH:$(realpath AnimalDetection/CameraTraps):$(realpath AnimalDetection/ai4utils)"
export PYTHONPATH="$PYTHONPATH:$(realpath smalst/external/neural_renderer/neural_renderer)"
