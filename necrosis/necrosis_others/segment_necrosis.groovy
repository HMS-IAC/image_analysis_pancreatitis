////// Merge Endocrine
//selectObjectsByClassification("Endocrine")
//mergeSelectedAnnotations()
//fireHierarchyUpdate()
//
//exoAnnotation = getAnnotationObjects().find{it.getPathClass() == getPathClass("Exocrine")}
//exoroi = exoAnnotation.getROI()
//
////// draw bounding box around exocrine
//x = exoroi.getBoundsX()
//y = exoroi.getBoundsY()
//width = exoroi.getBoundsWidth()
//height = exoroi.getBoundsHeight()
//
//roi = ROIs.createRectangleROI(x, y, width, height, ImagePlane.getDefaultPlane())
//def pathObject = PathObjects.createAnnotationObject(roi, getPathClass("exoBB") )
//addObject(pathObject) 
//
//selectObjectsByClassification("exoBB")
selectObjectsByClassification("Exocrine")
createAnnotationsFromPixelClassifier("necrosis_ignorebackground", 150.0, 50.0)
   
