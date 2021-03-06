# -*- coding: utf-8 -*-
import os
import h5py
import numpy as np
import matplotlib.pyplot as plt
from skimage import morphology,data,color
from PIL import Image
from tqdm import tqdm

def write_hdf5(data, out_file):
    with h5py.File(out_file, 'w') as file:
        file.create_dataset('data', data=data, dtype=data.dtype)

def skeletonize():
    image=color.rgb2gray(data.horse())
    image=1-image # Invert
    skeleton =morphology.skeletonize(image)

    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(8, 4))
    ax1.imshow(image, cmap=plt.cm.get_cmap('gray'))
    ax1.set_title('original', fontsize=15)
    ax1.axis('off')
    ax2.imshow(skeleton, cmap=plt.cm.get_cmap('gray'))
    ax2.set_title('skeleton', fontsize=15)
    ax2.axis('off')
    fig.tight_layout()
    plt.show()

def process_data(original_image_dir, ground_truth_dir, border_mask_dir):
    original_images = []
    ground_truths = []
    border_masks = []

    _, _, original_image_paths = list(os.walk(original_image_dir))[0]
    _, _, ground_truth_paths = list(os.walk(ground_truth_dir))[0]
    _, _, border_mask_paths = list(os.walk(border_mask_dir))[0]

    for i in tqdm(range(len(original_image_paths)), ascii=True):
        original_image = Image.open(original_image_dir + original_image_paths[i])
        ground_truth = Image.open(ground_truth_dir + ground_truth_paths[i])
        border_mask = Image.open(border_mask_dir + border_mask_paths[i])
        original_images.append(np.asarray(original_image))
        ground_truths.append(np.asarray(ground_truth))
        border_masks.append(np.asarray(border_mask))

    original_images = np.array(original_images)
    ground_truths = np.array(ground_truths)
    border_masks = np.array(border_masks)

    ground_truths = (ground_truths/255).astype(np.uint8)
    border_masks = (border_masks/255).astype(np.uint8)

    original_images = np.reshape(original_images, (-1, 584, 565, 3))
    ground_truths = np.reshape(ground_truths, (-1, 584, 565, 1))
    border_masks = np.reshape(border_masks, (-1, 584, 565, 1))
    return original_images, ground_truths, border_masks

if __name__ == '__main__':
    preprocessed_dir = './data/DRIVE_preprocessed/'
    train_original_image_dir = './data/DRIVE/training/images/'
    train_ground_truth_dir = './data/DRIVE/training/1st_manual/'
    train_border_mask_dir = './data/DRIVE/training/mask/'
    test_original_image_dir = './data/DRIVE/test/images/'
    test_ground_truth_dir = './data/DRIVE/test/1st_manual/'
    test_border_mask_dir = './data/DRIVE/test/mask/'

    # 1\ Make a dir to save preprocessed data.
    if not os.path.exists(preprocessed_dir):
        os.makedirs(preprocessed_dir)

    # 2\ Save train data.
    train_original_image, train_ground_truth, train_border_mask = process_data(
        train_original_image_dir, train_ground_truth_dir, train_border_mask_dir)
    write_hdf5(train_original_image, preprocessed_dir + 'DRIVE_train_original_image.hdf5')
    write_hdf5(train_ground_truth, preprocessed_dir + 'DRIVE_train_ground_truth.hdf5')
    write_hdf5(train_border_mask, preprocessed_dir + 'DRIVE_train_border_mask.hdf5')
    print('There are {} images for training.'.format(len(train_original_image), ))

    # 3\ Save test data.
    test_original_image, test_ground_truth, test_border_mask = process_data(
        test_original_image_dir, test_ground_truth_dir, test_border_mask_dir)
    write_hdf5(test_original_image, preprocessed_dir + 'DRIVE_test_original_image.hdf5')
    write_hdf5(test_ground_truth, preprocessed_dir + 'DRIVE_test_ground_truth.hdf5')
    write_hdf5(test_border_mask, preprocessed_dir + 'DRIVE_test_border_mask.hdf5')
    print('There are {} images for testing.'.format(len(test_original_image)))