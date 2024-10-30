setImageType('BRIGHTFIELD_H_E');


// Annotations named "Region*" were small manually drawn regions used to generate a composite image 
resetSelection();
selectObjectsByClassification("Region*");
clearSelectedObjects(true);

selectAnnotations();
createAnnotationsFromPixelClassifier("endo_exo_bin_20240521", 1500.0, 1500.0)


