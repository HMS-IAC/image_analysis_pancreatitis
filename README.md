# Image analysis of pancreatitis 
## Prerequisites
Python, conda, QuPath

## Types of files
**.json** or **.json.zip**: Pixelclassifiers that were trained in QuPath and saved as .json file. **.json.zip** can be unzipped to obtain **.json**.  
For documentation on how to train pixel classifiers see [here](https://qupath.readthedocs.io/en/stable/docs/tutorials/pixel_classification.html).  

**.groovy**: Groovy script. Can be run in [QuPath](https://qupath.readthedocs.io/en/stable/docs/scripting/workflows_to_scripts.html). For information on how to apply a groovy script on multiple images, see [here](https://qupath.readthedocs.io/en/stable/docs/scripting/workflows_to_scripts.html#running-a-script-for-multiple-images).  

**.py**: python files  

**environment.yml**: contains conda environment under which .py files in this repository can run. Information from how to create an invironment from environment.yml can be found [here](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file).  

## CD11B
Contains pixel-classifiers to segment tissue and CD11b+ cells in IHC slices of the pancreas 

## tissue_segmentation_general
Contains files to segment exocrine and endocrine tissue 

## Training_images 
Contains .groovy files to randomly select a square tissue area within a bounding box. When applied to multiple images, all such-annotated regions can be combined into a composite image for training. 
(See [here](https://qupath.readthedocs.io/en/stable/docs/tutorials/pixel_classification.html#create-a-training-image) for instructions)

## tissue_segmentation_general
**fine_grained_segmentation.groovy** applies the pixel classifier **endo_exo_bin_20240521.json** to segment endocrine and exocrine tissue. 
**coarse_grained_segmentation.groovy** simplifies the segments.  
**background.json** allows to remove white background from the exocrine segment. 


## edema 
**refine_exocrine.groovy** segments edema within exocrine segments  
**export_edema_experimental.groovy** generates mask images (png) of exocrine tissue and segmented edema  
**tile_image.py** reads png images and generates non-overlapping tiles of them (saved as images in a specified output folder)
**edema_to_graph_downsampled.py** counts the number of branchpoints for each sample 

## necrosis 
### 14550 and 25868
For samples 14550 and 25868, tissue segmentation from the preveous edema segmentation were reused.  
**clearedema.groovy** removes segmented edema  
**segment_necrosis.groovy** loads the pixelclassifier necrosis_ignorebackground.json and segments necrosis.  
**mergenecrosis.groovy** assignes pixels that are both classified as necrosis and endocrine to only endocrine  
**export_necrosis.groovy** exports area-values of necrosis as a .csv file  

### 11571
**exocrine11571.json** was trained on samples of batch 11571. Exocrine tissue was segmented within the previous exocrine bounding box (excluding previous endocrine tissue).  
**new_exocrine.groovy** subtracts white background segmented with **background.json** from exocrine segments.  
**necrosis2.json** was trained on 11571 and applied to segment necrosis within the exocrine region (**segment_necrosis.groovy**).  
**export_necrosis.groovy** exports areas-values of necrosis as a .csv file  
