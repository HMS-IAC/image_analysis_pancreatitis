
fluid = getAnnotationObjects().findAll{it.getPathClass() == getPathClass("fluid")}

if (!fluid) { // If Edema was not already segmented
    
    clearDetections();
    
    
    // Merge Endocrine
    selectObjectsByClassification("Endocrine")
    mergeSelectedAnnotations()
    fireHierarchyUpdate()
    
    exoAnnotation = getAnnotationObjects().find{it.getPathClass() == getPathClass("Exocrine")}
    exoroi = exoAnnotation.getROI()
    
    // draw bounding box around exocrine
    x = exoroi.getBoundsX()
    y = exoroi.getBoundsY()
    width = exoroi.getBoundsWidth()
    height = exoroi.getBoundsHeight()
    
    roi = ROIs.createRectangleROI(x, y, width, height, ImagePlane.getDefaultPlane())
    def pathObject = PathObjects.createAnnotationObject(roi, getPathClass("exoBB") )
    addObject(pathObject) 
    
    selectObjectsByClassification("exoBB")
    
    // generate background class in bounding box 
    println("generating background class")
    createAnnotationsFromPixelClassifier("background", 1500.0, 20.0)
    fireHierarchyUpdate()
    
    
    
    subtract = ["Endocrine", "background"]
    for (i in subtract){  
        // Get Geometry of Exocrine to remove overlap with Endocrine or background. 
        // Overlap will be removed from Exocrine and kept at Endocrine or background. 
        exoAnnotation = getAnnotationObjects().find{it.getPathClass() == getPathClass("Exocrine")}
        exoGeom = exoAnnotation.getROI().getGeometry()
        
        
        
        // Get Geometry of Endocrine
        sbtAnnotation = getAnnotationObjects().find{it.getPathClass() == getPathClass(i)}
        sbtGeom = sbtAnnotation.getROI().getGeometry()
        
        // Remove the old Exocrine annotation
        exoAnnotation = getAnnotationObjects().findAll{it.getPathClass() == getPathClass("Exocrine")}
        println(exoAnnotation)
        removeObjects(exoAnnotation, true)
        fireHierarchyUpdate()
        
        // Remove Endocrine overlap from Exocrine annotation
        exoNew = exoGeom.difference(sbtGeom)
        
        
        
        //finalize: Turn updated Exocrine into annotation 
        exoNewROI = GeometryTools.geometryToROI(exoNew, ImagePlane.getDefaultPlane())
        makeexonew = PathObjects.createAnnotationObject( exoNewROI, getPathClass("Exocrine") )
        addObject(makeexonew)
        
        fireHierarchyUpdate()
        
    }
    
    // shrink exocrine by 1 micron
    selectObjectsByClassification("Exocrine")
    runPlugin('qupath.lib.plugins.objects.DilateAnnotationPlugin', '{"radiusMicrons":-1.0,"lineCap":"ROUND","removeInterior":false,"constrainToParent":true}')
    
    // Find parent annotation (level == 0), aka annotation created in step 1
    def firstAnnotation = getAnnotationObjects().findAll{it.getLevel() == 1 && it.getPathClass() == getPathClass('Exocrine')}
    
    // Remove parent annotation
    removeObjects(firstAnnotation, true)
    
    
    fireHierarchyUpdate()
    
    selectObjectsByClassification("Exocrine")
    runPlugin('qupath.lib.plugins.objects.RefineAnnotationsPlugin', '{"minFragmentSizeMicrons":2000.0,"maxHoleSizeMicrons":0.0}')
    
    fireHierarchyUpdate()
    
    selectObjectsByClassification("Exocrine")
    createAnnotationsFromPixelClassifier("edema_20241006", 5.0, 15.0) // generate edema segmentation
    fireHierarchyUpdate()
}