import numpy as np 
from skimage import io, morphology, measure
from scipy.ndimage import convolve
import napari
from PIL import Image
import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import shapiro
import scipy.stats as stats
Image.MAX_IMAGE_PIXELS = 1000000000


parent_folder = '/path/to/tiles/'
downsampled = 1.5
pxsize_org = 0.252 # original pixel size in microns per pixel
pxsize = downsampled * pxsize_org # originally 0.252 microns per pixel, downsampled x 1.5


def process(image):
    # check whether edema color is 68 or 182. This is the value exported by QuPath and can be checked with Fiji. 
    if not 182 in image:
        binary_image = image == 68
    else: 
        binary_image = image == 182

    # Skeletonize the image
    skeleton = morphology.skeletonize(binary_image)


    def count_branch_points(skeleton):
        # Define the kernel to find branch points
        kernel = np.array([[1, 1, 1],
                        [1, 10, 1],
                        [1, 1, 1]])

        # Convolve the skeleton image with the kernel
        convolved = convolve(skeleton.astype(int), kernel)

        # Identify branch points (pixels with more than 3 neighbors)
        branch_points = (convolved > 12)

        # Label connected components in the branch_points image
        labeled_branch_points = measure.label(branch_points)

        # Count the number of branch points
        branch_point_count = np.max(labeled_branch_points)

        return branch_point_count, labeled_branch_points


    n_branch_points, _ = count_branch_points(skeleton)
    #print("Number of branch points:", num_branch_points)

    return n_branch_points



    # # Visualize the image
    # viewer = napari.Viewer()
    # viewer.add_image(image_exo, name = 'exo')
    # viewer.add_image(binary_image, name = 'binary')
    # viewer.add_image(skeleton, name = 'skeleton')
    # viewer.add_image(convolved, name = 'convolved')
    # viewer.add_image(branch_points, name = 'branch points')
    # viewer.add_image(labeled_branch_points, name = 'branch points label')


    # napari.run()

def processexo(image_exo):
    return np.count_nonzero(image_exo == 72)

def read_images(input_dir, process, processexo):
    # Get list of image files
    tiles = glob.glob(os.path.join(input_dir, 'tile_*.png'))  # Adjust the pattern as needed
    exo = glob.glob(os.path.join(input_dir, 'exotile_*.png'))
    print(tiles)
    allbranchpoints = 0
    allpixels = 0

    for image_path, exo_path in zip(tiles, exo):
        # Open the image
        tile = io.imread(image_path)
        exo_tile = io.imread(exo_path)
        # Process the image
        branchpoints = process(tile)
        pixels = processexo(exo_tile)
        allbranchpoints += branchpoints
        allpixels += pixels
    return allbranchpoints, allpixels


def list_folders(parent_folder):
    # Use glob to find all directories in the parent folder
    folders = [f + "/tiles" for f in glob.glob(os.path.join(parent_folder, '*')) if os.path.isdir(f)]
    return folders

# Usage
folders = list_folders(parent_folder)

bps = []
pxs = []
bpppx = []
foldername = [] 

for folder in folders:
    if os.path.exists(folder):

        allbranchpoints, allpixels = read_images(folder, process, processexo)
        bps.append(allbranchpoints)
        pxs.append(allpixels)
        foldername.append(folder)
        bpppx.append(allbranchpoints/allpixels)

area = [px * pxsize**2 for px in pxs]
bppa = [bp/a for bp, a in zip(bps, area)]
data = {'folder': foldername, 'branchpoints': bps, 'pixels': pxs, 'area': area, 'bpp': bpppx, 'bppa': bppa}
bpdata = pd.DataFrame(data)


def filterfor(pattern, df):
    return df[df["folder"].str.contains(pattern)]


def areaweight(df, type = 'pixels'): 
    total_a = np.sum(df[type])
    total_b = np.sum(df['branchpoints'])
    return total_b/total_a

def getlowSEM(results, type = 'bpp'):
    return np.mean(results[type]) - stats.sem(results[type])

def gethighSEM(results, type = 'bpp'):
    return np.mean(results[type]) + stats.sem(results[type])

def plotviolin(columns, xticks = ['PBS', 'Caer', 'Treatment', 'Prophylaxis'], type = 'bppa'):
    
    type2 = 'area' if type == 'bppa' else 'pixels'
    ylabel = 'Branch points per area [$\mu^{-2}$]' if type == 'bppa' else 'Branch points per pixel'
    
    fig, ax = plt.subplots()
    violins = ax.violinplot([column[type] for column in columns], showmeans=True)

    linec = 'dimgrey'
    violins['cbars'].set_edgecolor(linec)
    violins['cmins'].set_edgecolor(linec)
    violins['cmaxes'].set_edgecolor(linec)
    violins['cmeans'].set_edgecolor(linec)

    for i, column in enumerate(columns):
        ax.scatter(np.random.normal(i+1, 0.05, len(column[type])), column[type], c = 'k')
        ax.scatter(i+1, areaweight(column, type = type2), c='blue', marker='D')
        # ax.hlines(areaweight(column, type = type2), i+0.9, i+1.1, color='blue')
        ax.hlines(getlowSEM(column, type = type), i+0.9, i+1.1, color='red')
        ax.hlines(gethighSEM(column, type = type), i+0.9, i+1.1, color='red')

    for body in violins['bodies']:
        body.set_facecolor('gray')

    ax.set_ylabel(ylabel)
    ax.set_xticks([i+1 for i in range(len(columns))], xticks)
    plt.show()

##
batch11571 = filterfor('11571', bpdata)
healthy11571 = filterfor('Group1', batch11571)
sick11571 = filterfor('Group2', batch11571)
bpti11571 = filterfor('Group3', batch11571)
spink11571 = filterfor('Group4', batch11571)

columns = [healthy11571, sick11571, bpti11571, spink11571]
plotviolin(columns, xticks = ['Healthy', 'Sick', 'FC-BPTI', 'FC-SPINK1'], type = 'bppa')

# No 2-5 bppa
columns = [healthy11571, sick11571[sick11571['bppa'] > 0.0013], bpti11571, spink11571]
plotviolin(columns, xticks = ['PBS', 'Caer', 'FC-BPTI', 'FC-SPINK1'], type = 'bppa')


# No 2-5 bpp
sick_no25 = sick11571[sick11571['bpp'] > 0.00018]
columns = [healthy11571, sick_no25, bpti11571, spink11571]
plotviolin(columns, xticks = ['PBS', 'Caer', 'FC-BPTI', 'FC-SPINK1'], type = 'bpp')



def logodds(results): 
    p = results/100
    q = 1 - p 
    return p/q

def welchs(one, two, logodds, message = None):
    odds1 = logodds(one)
    odds2 = logodds(two)
    if message:
        print(message)
    print(stats.ttest_ind(odds1, odds2, alternative='greater', equal_var=False))


def mannwhitnye(one, two, message = None):
    if message:
        print("MWU: ", message)
    print(stats.mannwhitneyu(one, two, alternative='greater', method='exact'))

sickall = pd.concat([sick_no25, bpti11571])

print('sick, no 2-5', shapiro(sick_no25['bppa']))
print('sick, no 2-5 _ bpti: ', shapiro(sickall['bppa']))
print('spink: ', shapiro(spink11571['bppa']))
print('bpti: ', shapiro(bpti11571['bppa']))
print('healthy: ', shapiro(healthy11571['bppa']))




welchs(sickall['bppa'], spink11571['bppa'], logodds, "sick + bpti vs spink")
welchs(sickall['bppa'], healthy11571['bppa'], logodds, "sick + bpti vs healthy")
welchs(sick_no25['bppa'], spink11571['bppa'], logodds, "sick vs spink")
welchs(sick_no25['bppa'], bpti11571['bppa'], logodds, "sick vs bpti")

