//// Written in QuPath 0.2.0-m11
//def newClass = getPathClass("NewClass")   // Your new class here
//def necr = getPathClass("Necrosis")
//
//getAnnotationObjects().each { annotation ->
//    if (annotation.getPathClass().equals(necr))
//        annotation.setPathClass(newClass)
//}
//fireHierarchyUpdate() // If you want to update the count in the Annotation pane
//
//print "Done!"


selectObjectsByClassification("Exocrine")
createAnnotationsFromPixelClassifier('necrosis2', 125.0, 75.0)
   
//