// exoBB is an annotation that is the bounding box of tissue. This speeds up segmentation, as only areas 
// within exoBB are segmented. exoBB can be drawn manually
selectObjectsByClassification("exoBB") 
createAnnotationsFromPixelClassifier("tissue_ignorebg", 2000.0, 1500.0) // generate tissue segmentation ('Exocrine')

selectObjectsByClassification("Exocrine")
createAnnotationsFromPixelClassifier("immune_cells_ignorebg", 15.0, 10.0) // generate immune cell segmentation
fireHierarchyUpdate()
