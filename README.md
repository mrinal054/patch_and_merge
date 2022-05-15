## Patch and Merge 
1. Can create patches from both 2D and 3D images
2. Can merge 2D or 3D patches 

As for 3D, the primary focus is 3D CT data. The data should be converted to an array before making 3D patches. 

So, the 2D image or 3D volume is needed to convert to an array first.

### How to install
```
pip install jenti
```

### How to import
```
from jenti.patch import Patch, Merge
```

### How to use
Sample demonstration on how to use this code is given in `test.py` and `test.ipynb`.

**Create patches from a 2D image**
```python
# Read image
im = Image.open('c.jpg') # color image
im.show()
image = np.array(im) # convert to array

# Create patches
patch_shape = [100, 100]
overlap = [10,10] # overlap between two adjacent patches along both axes
patch = Patch(patch_shape, overlap, patch_name='patch2d', csv_output=True)
patches, info, org_shape = patch.patch2d(image)

# Save patches       
patch.save2d(patches, save_dir='./save2d', ext = '.png')
```
If the `csv_output` is set to `True`, then it will save the locations of each patch 
in the original image in a `csv` file. </br>
Patch names will be like: `xxxx0000`, `xxxx0001`, `xxxx0002`, and so on.


**Create patches from a 3D volume**
```python
# Read volume
data = sio.loadmat('volume.mat')
data = data['data'] # shape: 128 x 128 x 50  x 1

# Create patches
patch_shape = [32, 32, 16, 1] # H x W x D x Ch
overlap = [8, 8, 8, 0]
patch = Patch(patch_shape, overlap, patch_name='patch3d', csv_output=True)
patches, info, org_shape = patch.patch3d(data)

# Save patches
patch.save3d(patches, save_dir='./save3d', ext = '.mat')
```

**Merge 2D patches**</br>
Merging can be done in two ways.</br>
Method 1: Read all the patch files first, then merge them together.
```python
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
merged_im = Image.fromarray(merged)
merged_im.show()
merged_im.save('merged2d.png')
```
Method 2: Provide only the patch directory.
```python
merge = Merge(info, org_shape, dtype='uint8')
merged = merge.merge_from_dir2d('./save2d') 
merged_im = Image.fromarray(merged)
merged_im.show()
merged_im.save('merged2d.png')
```
**Merge 3D patches**</br>
Method 1: Read all the patch files first, then merge them together.
```python
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
sio.savemat('merged3d.mat', {'m': merged}, do_compression=True)
```
Method 2: Provide only the patch directory.
```python
merge = Merge(info, org_shape, dtype='float32')
merged = merge.merge_from_dir3d('./save3d') 
sio.savemat('merged3d.mat', {'m': merged}, do_compression=True)
```
