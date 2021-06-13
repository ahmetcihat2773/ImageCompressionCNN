import os,sys,random,shutil

#from skimage.measure import compare_ssim

#from skimage.metrics import structural_similarity as ssim

#import skimage

import numpy as np

import cv2

import math

import numpy as np

import cv2

import imagecodecs
class ImageCompression():

    def __init__(self):

        self.input_folder = "/4288-2848" 

        print("IMAGE COMPRESSION IS STARTED")

    def find_resolution(self,resolution,same_file_size = False,same_ssmi = False):

        """

        This method finds different image resolutions in a folder and moves the 

        images which has the same resolution most to a folder.

        """

        #self.current_dir = os.getcwd()

        #self.dataset_dir = self.current_dir + "\dataset" 

        self.dataset_dir = "/4288-2848"        

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

        current_file_size = 0

        current_quality = 0

        for filename in os.listdir("4288-2848"):

            if ".tiff" in filename:                

                outfolder = "4288-2848_"+compression_type+"_UP_"+str(up_lim)+"_DOWN_"+str(down_lim)+"/"

                filename_save = filename.split(".")[0]

                # filename_save is like Image_101

                # filename comes like Image_101.tiff

                outfile = filename_save+"_"+str(number) + "."+compression_type 

                outfile = outfolder + outfile

                useless_file = filename_save+"_"+str(number) + "-1.jpeg"

                useless_file = outfolder + useless_file

                filename = "4288-2848/" + filename

                #outfile is the directory.    

                if not os.path.exists(outfolder):

                    os.makedirs(outfolder) 

                    

                # If not the folder is created just create the folder to save the output files. 

                # Compress the file for initial file size.

                for quality in range(40,100):                  

                    cmd = "convert -quality "+ str(quality)+" "+ filename +" "+ outfile

                    # 'cons_rcp.exe -s Image_1.tiff -o 4288-2848_jxr_UP_1228800_DOWN_1024000/Image_1_0.jxr -jxr_quality 0'

                    os.system(cmd)

                    os.remove(useless_file)

                    compressed_file = outfolder + filename_save+"_"+str(number) + "-0.jpeg"

                    compressed_size = os.stat(compressed_file).st_size

                    print(compressed_size)

                    print(quality)



                    if compressed_size >= down_lim and compressed_size <= up_lim:

                        # If the file size in range we want

                        break

                

                    else:

                        os.remove(compressed_file)

                    if compressed_size > up_lim:

                        os.remove(compressed_file)

                        break

            number = number + 1

                    

    def same_quality_jpeg2000(self,desired_quality):

        # https://github.com/uclouvain/openjpeg/issues/891

        # 1024 bytes = 1kbyte

        number = 0

        #current_dir = os.getcwd()

        current_file_size = 0

        current_quality = 0

        """

        Try all qualities from 0 to 100. If you get the desired quality continue with the next file.

        1. Convert tiff to jpeg,jpeg2000 

        2. Convert compressed jpeg,jpeg2000 to tiff

        3. Use this two tiff and calculate the ssim if between desired range remove the last tiff and continue with jpeg

        4. Else remove jpeg and tiff and use different quality parameter compress againd and continue with step 2.

        """        

        outfolder = "4288-2848_jp2_samequality_"+str(int(10*desired_quality))+"/"

        # '4288-2848_jpeg_samequality_7/'

        if not os.path.exists(outfolder):

            os.makedirs(outfolder)

        # This number indicates the number of images that is tried.

        dataset_dir = os.listdir("4288-2848_tif")

        for filename in dataset_dir:  

            if ".tif" in filename:

                # read tiff files from 4288-2848 

                save_name = filename.split(".")[0]

                # save_name has the name of the image before .tiff like Image_1

                compressed_file = save_name+"_"+str(number) + "."+"jp2"

                #This like Image_1_0.jpeg

                filename = "4288-2848_tif/"+filename

                                       

                compressed_file = outfolder + compressed_file

                # compressed_file :: 4288-2848_jpeg_samequality_7/Image_1_0.jpeg

                converted_tiff_dir = outfolder+save_name+"_"+str(number) + "."+"tif"

                # converterd_tiff_dir :: 4288-2848_jpeg_samequality_7/Image_1_0.tiff

                

                for temp_quality in range(30,2,-3):

                    print("TEMP QUALITY",temp_quality)

                    compressed_file = save_name+"_"+str(number) + ".jp2"

                    compressed_file = outfolder + compressed_file

                    cmd = "opj_compress -i "+ filename +" -o "+ compressed_file +" -q " + str(temp_quality) 

                    os.system(cmd)

                    # Compress the tiff to jpeg,jpeg2000.

                    compressed_file = compressed_file.split(".")[0]

                    

                    compressed_file = compressed_file + ".jp2"

                    cmd = "opj_decompress -i "+ compressed_file +" -o "+ converted_tiff_dir 

                    os.system(cmd)

                    # convert jpeg to tiff back.

                    ssim_val = self.calculate_ssim(filename,converted_tiff_dir)

                    if ssim_val >= desired_quality - 0.03 and ssim_val<= desired_quality + 0.03:

                        

                        os.remove(converted_tiff_dir)                       

                        break

                    else:

                        os.remove(compressed_file)

                        os.remove(converted_tiff_dir)

                    if ssim_val < desired_quality - 0.03:

                        break

                print(ssim_val)

            number = number + 1

    def same_quality_jxr(self,desired_quality):
        """
        To read the JPEG XR we are using imagecodecs library as follow.
        #data = open('Image_1_0.jxr', 'rb').read()
        #im = imagecodecs.jxr_decode(data)       
        https://stackoverflow.com/questions/51442437/jpeg-decompression-on-raw-image-in-python
        XnConvert program covnert the JXR TO TIFF and it only changes the extension so it does not add any number to the 
        JXR name.
        """
        number = 0
        current_file_size = 0
        current_quality = 0
        outfolder = "4288-2848_jxr_samequality_"+str(int(10*desired_quality))+"/"
        # '4288-2848_jpeg_samequality_7/'
        if not os.path.exists(outfolder):
            os.makedirs(outfolder)
        # This number indicates the number of images that is tried.
        dataset_dir = os.listdir("4288-2848/")
        for filename in dataset_dir:  
            if ".tiff" in filename:
                # read tiff files from 4288-2848 
                save_name = filename.split(".")[0]
                # save_name has the name of the image before .tiff like Image_1
                compressed_file = save_name+"_"+str(number) + "."+"jxr"
                compressed_file = outfolder + compressed_file
                #This like Image_1_0.jpeg
                filename = "4288-2848/"+filename
                # compressed_file :: 4288-2848_jpeg_samequality_7/Image_1_0.jpeg
                converted_tiff_dir = outfolder+save_name+"_"+str(number) + "."+"tiff"
                # converterd_tiff_dir :: 4288-2848_jpeg_samequality_7/Image_1_0.tiff

                for temp_quality in range(30,2,-2):   

                    print("TEMP QUALITY",temp_quality)
                    cmd = "cons_rcp.exe -s "+ filename + " -o "+ compressed_file + " -jxr_quality " +str(temp_quality)
                    #cmd = "nconvert -out jxr -q "+ str(temp_quality) +" -o " +compressed_file+ " " + filename 
                    os.system(cmd)
                    # Compress the tiff to jpeg,jpeg2000.
                    compressed_file = compressed_file.split(".")[0]
                    compressed_file = compressed_file + ".jxr"
                    cmd = "nconvert -out tiff -o "+  converted_tiff_dir +" " + compressed_file
                    os.system(cmd)
                    # convert jpeg to tiff back.
                    imageA = cv2.imread(filename)
                    imageB = cv2.imread(converted_tiff_dir)
                    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
                    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
                    ssim_val = self.calculate_ssim_1(grayA,grayB)
                    print("SSIM VAL",ssim_val)
                    if ssim_val >= desired_quality - 0.03 and ssim_val<= desired_quality + 0.03:
                        os.remove(converted_tiff_dir) 
                        break
                    else:
                        os.remove(compressed_file)
                        os.remove(converted_tiff_dir)
                    if ssim_val < desired_quality - 0.03:
                        break
                print(ssim_val)
            number = number + 1

    def same_quality_jpeg(self,desired_quality):

        # https://github.com/uclouvain/openjpeg/issues/891

        # 1024 bytes = 1kbyte

        number = 0

        #current_dir = os.getcwd()

        current_file_size = 0

        current_quality = 0

        """

        Try all qualities from 0 to 100. If you get the desired quality continue with the next file.

        1. Convert tiff to jpeg,jpeg2000 

        2. Convert compressed jpeg,jpeg2000 to tiff

        3. Use this two tiff and calculate the ssim if between desired range remove the last tiff and continue with jpeg

        4. Else remove jpeg and tiff and use different quality parameter compress againd and continue with step 2.

        """        

        outfolder = "4288-2848_jpeg_samequality_"+str(int(10*desired_quality))+"/"

        # '4288-2848_jpeg_samequality_7/'

        if not os.path.exists(outfolder):

            os.makedirs(outfolder)

        # This number indicates the number of images that is tried.

        dataset_dir = os.listdir("4288-2848")

        for filename in dataset_dir:  

            if ".tiff" in filename:

                # read tiff files from 4288-2848 

                save_name = filename.split(".")[0]

                # save_name has the name of the image before .tiff like Image_1

                compressed_file = save_name+"_"+str(number) + ".jpeg"

                #This like Image_1_0.jpeg

                filename = "4288-2848/"+filename                                        

                compressed_file = outfolder + compressed_file

                # compressed_file :: 4288-2848_jpeg_samequality_7/Image_1_0.jpeg

                converted_tiff_dir = outfolder+save_name+"_"+str(number) + "."+"tiff"

                # converterd_tiff_dir :: 4288-2848_jpeg_samequality_7/Image_1_0.tiff

                

                for temp_quality in range(23,2,-3):

                    print("TEMP QUALITY",temp_quality)

                    compressed_file = save_name+"_"+str(number) + ".jpeg"

                    compressed_file = outfolder + compressed_file

                    self.run_command(filename,compressed_file,"jpeg",temp_quality)

                    # Compress the tiff to jpeg,jpeg2000.

                    compressed_file = compressed_file.split(".")[0]

                    useless_file = compressed_file + "-1.jpeg"

                    if "jpeg" in useless_file:

                        os.remove(useless_file)

                        compressed_file = compressed_file + "-0.jpeg"

                    else:

                        compressed_file = compressed_file + ".jpeg"

                    self.run_command(compressed_file,converted_tiff_dir,"tiff",0)

                    # convert jpeg to tiff back.

                    ssim_val = self.calculate_ssim(filename,converted_tiff_dir)

                    if ssim_val >= desired_quality - 0.1 and ssim_val<= desired_quality + 0.1:

                        

                        os.remove(converted_tiff_dir)

                       

                        break

                    else:

                        os.remove(compressed_file)

                        os.remove(converted_tiff_dir)

                print(ssim_val)

            number = number + 1   



    def run_command(self,inputfile,outfile,compression_type,quality):



        if compression_type == "tiff":

            cmd = "convert "+inputfile +" "+ outfile 

            os.system(cmd)

        else:                

            cmd = "convert -quality "+ str(quality)+" "+ inputfile +" "+ outfile 

            os.system(cmd)

    def calculate_ssim(self,tiff_1,tiff_2):

        #os.rename(tiff_1,tiff_1+"f")

        #os.rename(tiff_2,tiff_2+"f")

        #tiff_1 = tiff_1 + "f"

        #tiff_2 = tiff_2 + "f"

        imageA = cv2.imread(tiff_1)

        imageB = cv2.imread(tiff_2)

        grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)

        grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

        # 5. Compute the Structural Similarity Index (SSIM) between the two images, ensuring that the difference image is returned

        #(score, diff) = compare_ssim(grayA, grayB,full=True)

        #a = ffqm(grayA,grayB).calc(["ssim"])

        score = self.calculate_ssim_1(grayA,grayB)



        # 6. You can print only the score if you want

        print("SSIM: {}".format(score))

        return score

    def ssim_sen(self,img1, img2):
        C1 = (0.01 * 255)**2
        C2 = (0.03 * 255)**2
        img1 = img1.astype(np.float32)
        img2 = img2.astype(np.float32)
        kernel = cv2.getGaussianKernel(11, 1.5)

        window = np.outer(kernel, kernel.transpose())



        mu1 = cv2.filter2D(img1, -1, window)[5:-5, 5:-5]  # valid

        mu2 = cv2.filter2D(img2, -1, window)[5:-5, 5:-5]

        mu1_sq = mu1**2


        mu2_sq = mu2**2


        mu1_mu2 = mu1 * mu2

        sigma1_sq = cv2.filter2D(img1**2, -1, window)[5:-5, 5:-5] - mu1_sq

        sigma2_sq = cv2.filter2D(img2**2, -1, window)[5:-5, 5:-5] - mu2_sq

        sigma12 = cv2.filter2D(img1 * img2, -1, window)[5:-5, 5:-5] - mu1_mu2



        ssim_map = ((2 * mu1_mu2 + C1) * (2 * sigma12 + C2)) / ((mu1_sq + mu2_sq + C1) *

                                                                (sigma1_sq + sigma2_sq + C2))

        return ssim_map.mean()

    def calculate_ssim_1(self,img1, img2):

        '''calculate SSIM

        the same outputs as MATLAB's

        img1, img2: [0, 255]

        # https://cvnote.ddlee.cc/2019/09/12/psnr-ssim-python

        '''

        if not img1.shape == img2.shape:

            raise ValueError('Input images must have the same dimensions.')

        if img1.ndim == 2:

            return self.ssim_sen(img1, img2)

        elif img1.ndim == 3:

            if img1.shape[2] == 3:

                ssims = []

                for i in range(3):

                    ssims.append(self.ssim_sen(img1, img2))

                return np.array(ssims).mean()

            elif img1.shape[2] == 1:

                return self.ssim_sen(np.squeeze(img1), np.squeeze(img2))

        else:

            raise ValueError('Wrong input image dimensions.')