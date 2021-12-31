from PIL import Image
import numpy as np
from patch import Patch, Merge
import os
import pandas as pd
import scipy.io as sio

#%% For 2D
# Read image
im = Image.open('c.jpg') # color image
#im = Image.open('b.jpg') # binary image
#im = Image.open('g.jpg') # gray-scale image
im.show()
image = np.array(im) # convert to array

# Create patches
patch_shape = [100, 100]
overlap = [10,10]
patch = Patch(patch_shape, overlap, patch_name='patch2d', csv_output=True)
patches, info, org_shape = patch.patch2d(image)

# Save patches       
patch.save2d(patches, save_dir='./save2d', ext = '.png')

# Merge patches
names = os.listdir('./save2d')
patches = []
info = pd.read_csv('patch2d.csv')
info = np.array(info)
org_shape = (3024, 4032, 3)

for name in names:
    p = Image.open(os.path.join('./save2d', name))
    p = np.array(p)
    patches.append(p)
    
merge = Merge(info, org_shape, dtype='uint8')
merged = merge.merge2d(patches)
#merged = merge.merge_from_dir2d('./save2d') # uncomment to load from directory
merged_im = Image.fromarray(merged)
merged_im.show()
merged_im.save('merged2d.png')

#%% For 3D
# Read volume
data = sio.loadmat('volume.mat')
data = data['data'] # shape: 128 x 128 x 50  x 1

# Create patches
patch_shape = [32, 32, 16, 1]
overlap = [8, 8, 8, 0]
patch = Patch(patch_shape, overlap, patch_name='patch3d', csv_output=True)
patches, info, org_shape = patch.patch3d(data)

# Save patches
patch.save3d(patches, save_dir='./save3d', ext = '.mat')

# Merge patches
names = os.listdir('./save3d')
patches = []
info = pd.read_csv('patch3d.csv')
info = np.array(info)
org_shape = (128, 128, 50, 1)

for name in names:
    p = sio.loadmat(os.path.join('./save3d', name))
    p = p['p']
    patches.append(p)
    
merge = Merge(info, org_shape, dtype='float32')
merged = merge.merge3d(patches)
#merged = merge.merge_from_dir3d('./save3d') # uncomment to load from directory
sio.savemat('merged3d.mat', {'m': merged}, do_compression=True)

