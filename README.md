# Image analysis of pancreatitis 

## Types of files
**.json** or **.json.zip**: QuPath Pixel classifiers. Pixelclassifiers were trained in QuPath and saved as .json file.  
For documentation on how to train pixel classifiers see [here]{https://qupath.readthedocs.io/en/stable/docs/tutorials/pixel_classification.html}
**.groovy**: Groovy script. Can be run in [QuPath]{https://qupath.readthedocs.io/en/stable/docs/scripting/workflows_to_scripts.html}. For information on how to apply a groovy script on multiple images, see [here]{https://qupath.readthedocs.io/en/stable/docs/scripting/workflows_to_scripts.html#running-a-script-for-multiple-images}
**.py**: python files  
**environment.yml**: contains conda environment under which .py files in this repository can run. Information from how to create an invironment from environment.yml can be found [here]{https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file}  

## CD11B
Contains pixel-classifiers to segment tissue and CD11b+ cells in IHC slices of the pancreas 

## Training_images 
Contains .groovy files to randomly select a square tissue area within a bounding box. When applied to multiple images, all such-annotated regions can be combined into a composite image for training. 

## edema 

