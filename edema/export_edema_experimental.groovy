import qupath.lib.images.servers.LabeledImageServer
fluid = getAnnotationObjects().findAll{it.getPathClass() == getPathClass("fluid")}

if (fluid) { // If Edema was already segmented
    
    println(getAnnotationObjects())
    
    def imageData = getCurrentImageData()
    
    // Define output path (relative to project)
    def name = GeneralTools.getNameWithoutExtension(imageData.getServer().getMetadata().getName())
    def pathOutput = buildFilePath(PROJECT_BASE_DIR, 'export', name)
    mkdirs(pathOutput)
    
    // Define output resolution
    // double requestedPixelSize = 1.0
    
    // Convert to downsample. Factor of 1 means no downsampling. 
    double downsample = 1.0 //requestedPixelSize / imageData.getServer().getPixelCalibration().getAveragedPixelSize()
    
    // Create an ImageServer where the pixels are derived from annotations
    def edemaServer = new LabeledImageServer.Builder(imageData)
        .backgroundLabel(0, ColorTools.WHITE) // Specify background label (usually 0 or 255)
        .downsample(downsample)    // Choose server resolution; this should match the resolution at which tiles are exported
        .addLabel('fluid', 1)
        .multichannelOutput(false) // If true, each label refers to the channel of a multichannel binary image (required for multiclass probability)
        .build()
    
    def exoServer = new LabeledImageServer.Builder(imageData)
        .backgroundLabel(0, ColorTools.WHITE) // Specify background label (usually 0 or 255)
        .downsample(downsample)    // Choose server resolution; this should match the resolution at which tiles are exported
        .addLabel('Exocrine', 1)      // Choose output labels (the order matters!)
        .multichannelOutput(false) // If true, each label refers to the channel of a multichannel binary image (required for multiclass probability)
        .build()
    
    
    // Export things within the exocrine bounding box 
    annotation = getAnnotationObjects().find{it.getPathClass() == getPathClass("Exocrine")}
    def edema_region = RegionRequest.createInstance(edemaServer.getPath(), downsample, annotation.getROI())
    def exo_region = RegionRequest.createInstance(exoServer.getPath(), downsample, annotation.getROI())
    def exoPath = buildFilePath(pathOutput, 'Exo' + '.png') 
    def edemaPath = buildFilePath(pathOutput, 'Edema' + '.png')

    
    writeImageRegion(edemaServer, edema_region, edemaPath)
    writeImageRegion(exoServer, exo_region, exoPath)
 }