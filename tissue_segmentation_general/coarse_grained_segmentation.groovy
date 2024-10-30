// import for simplifying annotations 
import qupath.lib.roi.ShapeSimplifier

// Segmentation was previously done using endo_exo_bin_20240521 with slight manual corrections (see  project alldata_cleaned for more info.)
selectAnnotations();

//simplify annotations
double altitudeThreshold = 10.0
def pathObjects = getSelectedObjects().findAll { it.isAnnotation() }
    pathObjects.each {
        def roi = ShapeSimplifier.simplifyShape(it.getROI(), altitudeThreshold)
        it.setROI(roi)
    }
fireHierarchyUpdate()


// Find parent annotation (level == 0), aka annotation created in step 1
def firstAnnotation = getAnnotationObjects().findAll{it.getLevel() == 1}

// Remove parent annotation
removeObjects(firstAnnotation, true)
fireHierarchyUpdate()

// expand annotations by 15 microns to fill small gaps that are not holes 
runPlugin('qupath.lib.plugins.objects.DilateAnnotationPlugin', '{"radiusMicrons":15.0,"lineCap":"ROUND","removeInterior":false,"constrainToParent":false}')

resolveHierarchy() // Resolve Hierarchy
fireHierarchyUpdate()

// Shrink annotations by 15 microns to roughly their original size 
selectAnnotations();

runPlugin('qupath.lib.plugins.objects.DilateAnnotationPlugin', '{"radiusMicrons":-15.0,"lineCap":"ROUND","removeInterior":false,"constrainToParent":false}')


// Find and remove parent annotation 
firstAnnotation = getAnnotationObjects().findAll{it.getLevel() == 1}
removeObjects(firstAnnotation, true)

fireHierarchyUpdate()

// Get Geometry of Exocrine to remove overlap with Endocrine. 
// Overlap will be removed from Exocrine and kept at Endocrine. 
exoAnnotation = getAnnotationObjects().find{it.getPathClass() == getPathClass("Exocrine")}
exoGeom = exoAnnotation.getROI().getGeometry()

// Get Geometry of Endocrine
endoAnnotation = getAnnotationObjects().find{it.getPathClass() == getPathClass("Endocrine")}
endoGeom = endoAnnotation.getROI().getGeometry()

// Remove the old Exocrine annotation
exoAnnotation = getAnnotationObjects().findAll{it.getPathClass() == getPathClass("Exocrine")}
println(exoAnnotation)
removeObjects(exoAnnotation, true)
fireHierarchyUpdate()

// Remove Endocrine overlap from Exocrine annotation
exoNew = exoGeom.difference(endoGeom)

//finalize: Turn updated Exocrine into annotation 
exoNewROI = GeometryTools.geometryToROI(exoNew, ImagePlane.getDefaultPlane())
makeexonew = PathObjects.createAnnotationObject( exoNewROI, getPathClass("Exocrine") )
addObject(makeexonew)

fireHierarchyUpdate()

// Lock annotations
getAnnotationObjects().each{it.setLocked(true)}

