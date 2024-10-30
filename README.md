# Image analysis of pancreatitis 

## Types of files
.json or .json.zip: QuPath Pixel classifiers. Pixelclassifiers were trained in QuPath and saved as .json file. 
.groovy: Groovy script. Can be run in QuPath 
environment.yml: contains conda environment to run .py files
.py: python files 

## CD11B
Contains pixel-classifiers to segment tissue and CD11b+ cells in IHC slices of the pancreas 

## Training_images 
Contains .groovy files to randomly select a square tissue area within a bounding box. When applied to multiple images, all such-annotated regions can be combined into a composite image for training. 