// Get Geometry of Necrosis to remove overlap with Endocrine. 
// Overlap will be removed from Necrosis and kept at Endocrine. 
selectObjectsByClassification("Necrosis");
mergeSelectedAnnotations();
fireHierarchyUpdate()

necAnnotation = getAnnotationObjects().find{it.getPathClass() == getPathClass("Necrosis")}
necGeom = necAnnotation.getROI().getGeometry()

// Get Geometry of Endocrine
endoAnnotation = getAnnotationObjects().find{it.getPathClass() == getPathClass("Endocrine")}
endoGeom = endoAnnotation.getROI().getGeometry()

// Remove the old Necrosis annotation
necAnnotation = getAnnotationObjects().findAll{it.getPathClass() == getPathClass("Necrosis")}
println(necAnnotation)
removeObjects(necAnnotation, true)
fireHierarchyUpdate()

// Remove Endocrine overlap from Necrosis annotation
necNew = necGeom.difference(endoGeom)

//finalize: Turn updated Necrosis into annotation 
necNewROI = GeometryTools.geometryToROI(necNew, ImagePlane.getDefaultPlane())
makenecnew = PathObjects.createAnnotationObject( necNewROI, getPathClass("Necrosis") )
addObject(makenecnew)

fireHierarchyUpdate()