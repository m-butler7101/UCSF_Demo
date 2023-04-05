import os
import argparse
import pydicom as dicom
import cv2
import dicom2nifti

from MaskCreator import create_mask
from PathChecker import check_path

parser = argparse.ArgumentParser()
parser.add_argument("--dir_path", type=str, default="./dicom_data/", help='txt path to the parent directory containing each collective set of dicom files/image acquisitions')
parser.add_argument("--jpeg_dir_name", type=str, default="jpeg_images", help='name given to the directory containing the output jpeg files that were converted from dicom')
parser.add_argument("--mask_dir_name", type=str, default="mask", help='name given to the directory containing the mask dicom files')
parser.add_argument("--output_dir_name", type=str, default="output_data", help='name given to the parent directory containing all of the output files')

input_args = parser.parse_args()

input_parent_dir_path = input_args.dir_path
jpeg_dir_name = input_args.jpeg_dir_name
mask_dir_name = input_args.mask_dir_name
output_parent_dir_name = input_args.output_dir_name

output_parent_dir_path = os.path.join(os.path.abspath(os.path.join(input_parent_dir_path, os.pardir)), output_parent_dir_name) #Places the output data directory in the same directory as the input data directory
check_path(output_parent_dir_path)

dicom_dirs = os.listdir(input_parent_dir_path) #List of all the input dicom data directories

for dicom_dir_name in dicom_dirs: #Loops through each set of image acquisitions

    if dicom_dir_name not in os.listdir(output_parent_dir_path): #Skips over any input patient data that has already been processed by this algorithm 

        dicom_dir_path = os.path.join(input_parent_dir_path, dicom_dir_name)
        output_dir_path = os.path.join(output_parent_dir_path, dicom_dir_name)
        jpeg_dir_path = os.path.join(output_dir_path, jpeg_dir_name)
        mask_dir_path = os.path.join(output_dir_path, mask_dir_name)
        
        check_path(jpeg_dir_path)
        check_path(mask_dir_path)

        dicom_files = os.listdir(dicom_dir_path) #List of all the '.dcm' files within a given dicom directory

        for dicom_file_name in dicom_files: #Loops through each of the dicom files within the directory

            dicom_file_path = os.path.join(dicom_dir_path, dicom_file_name)
            mask_file_path = os.path.join(mask_dir_path, dicom_file_name)
            jpeg_file_path = os.path.join(jpeg_dir_path, dicom_file_name).replace('.dcm', '.jpg') #Maintains the original file name of each dicom file by merely replacing the extension
            
            dicom_data = dicom.dcmread(dicom_file_path) #An object containing attributes for all of the dicom information in a given dicom file
            dicom_image = dicom_data.pixel_array #A numpy array representing the dicom image's voxel data

            mask = create_mask(dicom_image) #Binary mask derived from the original dicom image

            dicom_data.PixelData = mask.tobytes() #Maintains all of the original dicom information and only replaces the raw dicom image data with the binary mask
            
            dicom_data.save_as(mask_file_path) #Saves the modified dicom image data/binary mask as a new dicom file
            cv2.imwrite(jpeg_file_path, dicom_image) #Saves the original dicom image as a jpeg file
            
        dicom2nifti.convert_directory(dicom_dir_path, output_dir_path) #Saves the entire stack of dicom files/slices as a single compressed nifti file
