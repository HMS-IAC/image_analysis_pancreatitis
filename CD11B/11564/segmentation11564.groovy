//createAnnotationsFromPixelClassifier("exocrine", 2000.0, 1500.0) // run if tissue not already segmented

selectObjectsByClassification("Exocrine")
createAnnotationsFromPixelClassifier("immune_cells", 15.0, 10.0) // min area 15, min hole area 10
fireHierarchyUpdate()
