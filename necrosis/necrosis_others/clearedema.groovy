subset = getAnnotationObjects().findAll{it.getPathClass() == getPathClass("fluid")}
removeObjects(subset, true)
fireHierarchyUpdate()