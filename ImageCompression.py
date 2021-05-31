import os,sys,random,shutil

from skimage.measure import compare_ssim
from skimage.metrics import structural_similarity as ssim
import skimage
import numpy as np
from cv2 import cv2
class ImageCompression():
    def __init__(self):
        self.input_folder = "4288-2848/" 
        print("IMAGE COMPRESSION IS STARTED")
    def find_resolution(self,resolution,same_file_size = False,same_ssmi = False):
        """
        This method finds different image resolutions in a folder and moves the 
        images which has the same resolution most to a folder.
        """
        self.current_dir = os.getcwd()
        self.dataset_dir = self.current_dir + "\dataset" 
        size_dic = {}
        print(self.dataset_dir)
        for filename in os.listdir(self.dataset_dir):
            filename = "dataset/" + filename
            if ".tiff" in filename:
                im = Image.open(filename)
                width, height = im.size
                im.close()
                width = str(width)
                height = str(height)
                dic_key = width + "," + height
                if not dic_key in size_dic:
                    size_dic[dic_key] = 1
                else:
                    size_dic[dic_key] += 1
        max_rsol = max(size_dic, key=size_dic.get)
        max_rsol = max_rsol.split(",")
        self.width = int(max_rsol[0])
        self.height = int(max_rsol[1])
        self.move_image() 
        """
        This function finds the different resolution inside a given folder.
        """
    def move_image(self):
        """
        This method moves the images into a folder.

        """
        for filename in os.listdir(self.dataset_dir):
            filename = "dataset/" + filename
            folder_name = "dataset_1"
            if ".tiff" in filename:
                im = Image.open(filename)
                width, height = im.size
                im.close()
                if self.width == width and self.height == height:
                    print(folder_name)
                    dest = shutil.move(filename,folder_name) 

    def compressImage_samesize(self,up_lim,down_lim,compression_type):
        # 1024 bytes = 1kbyte
        number = 0
        current_dir = os.getcwd()
        current_file_size = 0
        current_quality = 0
        for filename in os.listdir(current_dir+"\\4288-2848"):
            if ".tiff" in filename:                
                outfolder = "4288-2848_"+compression_type+"_UP_"+str(up_lim)+"_DOWN_"+str(down_lim)+"/"
                filename_save = filename.split(".")[0]
                # filename comes like Image_101.tiff
                outfile = filename_save+"_"+str(number) + "."+compression_type 
                outfile = outfolder + outfile
                filename = "4288-2848/"+filename
                #outfile is the directory.    
                if not os.path.exists(outfolder):
                    os.makedirs(outfolder) 
                # If not the folder is created just create the folder to save the output files. 
                # Compress the file for initial file size.
                for quality in range(1,100):                  
                    cmd = "cons_rcp.exe -s " +filename+ " -o "+outfile + " -"+compression_type +"_quality " + str(quality)
                    # 'cons_rcp.exe -s Image_1.tiff -o 4288-2848_jxr_UP_1228800_DOWN_1024000/Image_1_0.jxr -jxr_quality 0'
                    os.system(cmd)
                    compressed_size = os.stat(outfile).st_size
                    print(compressed_size)
                    print(quality)

                    if compressed_size >= down_lim and compressed_size <= up_lim:
                        # If the file size in range we want
                        break
                
                    else:
                        os.remove(outfile)

                    
    
    def compressImage_samequality(self,desired_quality,compression_type):
        # 1024 bytes = 1kbyte
        number = 0
        current_dir = os.getcwd()
        current_file_size = 0
        current_quality = 0
        """
        Try all qualities from 0 to 100. If you get the desired quality continue with the next file.
        1. Convert tiff to jpeg,jpeg2000 
        2. Convert compressed jpeg,jpeg2000 to tiff
        3. Use this two tiff and calculate the ssim if between desired range remove the last tiff and continue with jpeg
        4. Else remove jpeg and tiff and use different quality parameter compress againd and continue with step 2.
        """        
        outfolder = "4288-2848_"+compression_type+"_samequality_"+str(int(10*desired_quality))+"/"
        # '4288-2848_jpeg_samequality_7/'
        if not os.path.exists(outfolder):
            os.makedirs(outfolder)
        # This number indicates the number of images that is tried.
        for filename in os.listdir(current_dir+"\\4288-2848"):  
            if ".tiff" in filename:
                # read tiff files from 4288-2848 
                save_name = filename.split(".")[0]
                # save_name has the name of the image before .tiff like Image_1
                compressed_file = save_name+"_"+str(number) + "."+compression_type
                #This like Image_1_0.jpeg
                filename = "4288-2848/"+filename        
                                
                compressed_file = outfolder + compressed_file
                # compressed_file :: 4288-2848_jpeg_samequality_7/Image_1_0.jpeg
                converted_tiff_dir = outfolder+save_name+"_"+str(number) + "."+"tiff"
                # converterd_tiff_dir :: 4288-2848_jpeg_samequality_7/Image_1_0.tiff
                
                for temp_quality in range(99,2,-1):
                    compressed_file = save_name+"_"+str(number) + "."+compression_type
                    compressed_file = outfolder + compressed_file
                    self.run_command(filename,compressed_file,compression_type,temp_quality)
                    # Compress the tiff to jpeg,jpeg2000.
                    compressed_file = compressed_file.split(".")[0]
                    useless_file = compressed_file + "-1."+compression_type
                    os.remove(useless_file)
                    compressed_file = compressed_file + "-0."+compression_type
                    self.run_command(compressed_file,converted_tiff_dir,"tiff",0)
                    # convert jpeg to tiff back.
                    ssim_val = self.calculate_ssim(filename,converted_tiff_dir)
                    if ssim_val >= desired_quality - 0.2 and ssim_val<= desired_quality + 0.2:
                        os.remove(converted_tiff_dir)
                        break
                    else:
                        os.remove(compressed_file)
                        os.remove(converted_tiff_dir)

            number = number + 1   

    def run_command(self,inputfile,outfile,compression_type,quality):

        if compression_type == "tiff":
            cmd = "magick convert "+inputfile +" "+ outfile 
            os.system(cmd)
        else:                
            cmd = "magick convert -quality "+ str(quality)+" "+ inputfile +" "+ outfile 
            os.system(cmd)
    def calculate_ssim(self,tiff_1,tiff_2):
        imageA = cv2.imread(tiff_1)
        imageB = cv2.imread(tiff_2)
        grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
        grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
        # 5. Compute the Structural Similarity Index (SSIM) between the two images, ensuring that the difference image is returned
        (score, diff) = compare_ssim(grayA, grayB,full=True)
        diff = (diff * 255).astype("uint8")

        # 6. You can print only the score if you want
        print("SSIM: {}".format(score))
        return score