# from matplotlib import pyplot as plt
import numpy as np
import nibabel as nib
import sys
import os

def split_single_image(fname, save_folder, prefix=""):
    if (not os.path.isdir(save_folder)):
        os.mkdir(save_folder)
    full_img = nib.load(fname)
    full_img = np.array(full_img.dataobj)
    ax1, ax2, ax3 = full_img.shape
    len1 = ax1//4
    len2 = ax2//4
    len3 = ax3//2
    print(f"Creating image patches from {fname}. Creating the following files:")
    for i in range(ax1//len1):
        for j in range(ax2//len2):  
            for k in range(ax3//len3):
                ax1min = i*len1
                ax1max = (i+1)*len1
                ax2min = j*len2
                ax2max = (j+1)*len2
                ax3min = k*len3
                ax3max = (k+1)*len3
                filename = f"{prefix}ax1({ax1min}-{ax1max})ax2({ax2min}-{ax2max})ax3({ax3min}-{ax3max})"
                img = full_img[ax1min:ax1max, ax2min:ax2max, ax3min:ax3max]
                img = nib.Nifti1Image(img, np.eye(4))
                out_path = f"{save_folder}/{filename}.nii.gz"
                print(out_path)
                nib.save(img, out_path)

def split_images(image_folder, save_folder):
    if (not os.path.isdir(save_folder)):
        os.mkdir(save_folder)
    fnames = os.listdir(image_folder)
    for f in fnames:
        split_single_image(f"{image_folder}/{f}", f"{save_folder}/{f[:-7]}")
