
import qupath.lib.gui.commands.Commands;
import qupath.lib.roi.RoiTools.CombineOp;
import qupath.lib.roi.ShapeSimplifier 
//
selectObjectsByClassification("Exocrine")
clearSelectedObjects()


boundingbox = "exoBB"

// Subtract annotation1 from annotation2
//Get single object of each class
annotation1 = getAnnotationObjects().findAll{p -> p.getPathClass() == getPathClass("Endocrine")}[0]
annotation2 = getAnnotationObjects().findAll{p -> p.getPathClass() == getPathClass(boundingbox)}[0]

//Select one object, then the other, then subtract the two
getCurrentHierarchy().getSelectionModel().setSelectedObject(annotation1, true);
getCurrentHierarchy().getSelectionModel().setSelectedObject(annotation2, true);
Commands.combineSelectedAnnotations(getCurrentImageData(), CombineOp.SUBTRACT);
fireHierarchyUpdate()
print "Subtractions complete"

selectObjectsByClassification(boundingbox)
createAnnotationsFromPixelClassifier("exocrine11571", 2000.0, 750.0)
fireHierarchyUpdate()


    
selectObjectsByClassification(boundingbox)
// generate background class in bounding box 
println("generating background class")
createAnnotationsFromPixelClassifier("background", 1500.0, 20.0)
fireHierarchyUpdate()

    
    
subtract = ["background"]
for (i in subtract){  
    // Get Geometry of Exocrine to remove overlap with background. 
    // Overlap will be removed from Exocrine and kept at background. 
    exoAnnotation = getAnnotationObjects().find{it.getPathClass() == getPathClass("Exocrine")}
    exoGeom = exoAnnotation.getROI().getGeometry()
    
    
    
    // Get Geometry of background
    sbtAnnotation = getAnnotationObjects().find{it.getPathClass() == getPathClass(i)}
    sbtGeom = sbtAnnotation.getROI().getGeometry()
    
//    // Remove the old Exocrine annotation
    exoAnnotation = getAnnotationObjects().findAll{it.getPathClass() == getPathClass("Exocrine")}
    println(exoAnnotation)
    removeObjects(exoAnnotation, true)
    fireHierarchyUpdate()
    
    // Remove background overlap from Exocrine annotation
    exoNew = exoGeom.difference(sbtGeom)
    
    
    
    //finalize: Turn updated Exocrine into annotation 
    exoNewROI = GeometryTools.geometryToROI(exoNew, ImagePlane.getDefaultPlane())
    makeexonew = PathObjects.createAnnotationObject( exoNewROI, getPathClass("Exocrine") )
    addObject(makeexonew)
    
    fireHierarchyUpdate()
    
}

selectObjectsByClassification("background")
clearSelectedObjects()