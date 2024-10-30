import qupath.lib.roi.RectangleROI
import qupath.lib.objects.PathAnnotationObject
import qupath.lib.images.servers.ImageServer



int seed = -1
def rng = new Random()
if (seed >= 0)
    rng.setSeed(seed)

double sidelength = 200 // side-length of square ROI 

selectObjectsByClassification("Exocrine");
def selected = getSelectedObject()  



//def roi = selected?.getROI()
exoAnnotation = getAnnotationObjects().find{it.getPathClass() == getPathClass("Exocrine")}
exoroi = exoAnnotation.getROI()
println(exoroi.getClass())

def imageData=getCurrentImageData()
pixelwidth = imageData.getServer().getPixelCalibration().getPixelWidth()

println(pixelwidth)
pxsidelength = sidelength/pixelwidth


int count = 0
double x = 0
double y = 0


while (count < 1) {
    println count
    if (Thread.currentThread().isInterrupted()) {
        println 'Interrupted!'
        return
    }
    x = exoroi.getBoundsX() + rng.nextDouble() * exoroi.getBoundsWidth()
    y = exoroi.getBoundsY() + rng.nextDouble() * exoroi.getBoundsHeight()

    if (!exoroi.contains(x, y)) //if exoroi contains x, y, increase count 
        continue
    count++
}

roi = ROIs.createRectangleROI(x, y, pxsidelength, pxsidelength, ImagePlane.getDefaultPlane())
def pathObject = PathObjects.createAnnotationObject(roi, getPathClass("Region*") )
addObject(pathObject) 