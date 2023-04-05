import numpy as np

def create_mask(dicom_image):
    
    '''
    This function outputs a binary mask for the input image by:
    - Calculating the mean intensity of the input image
    - Assigning a value of "1" for any voxel value that's greater than the mean intensity of the image
    - Assigning a value of "0" for any voxel value that's less than or equal to the mean intensity of the image
    '''

    mask = np.zeros_like(dicom_image)

    mean_intensity = np.mean(dicom_image)

    mask[dicom_image > mean_intensity] = 1

    return mask
