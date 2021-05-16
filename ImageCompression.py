import os,sys,random,shutil
from PIL import Image 

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

    def compressImage_samequality(self,up_lim,down_lim,quality,same_quality,compression_type):
        # 1024 bytes = 1kbyte
        number = 0
        current_dir = os.getcwd()
        current_file_size = 0
        current_quality = 0
        for filename in os.listdir(current_dir+"\\4288-2848"):
            if ".tiff" in filename:
                if same_quality:
                    outfolder = "4288-2848_"+compression_type+"_samequality_"+str(quality)+"/"
                    if not os.path.exists(outfolder):
                        os.makedirs(outfolder)
                    filename_save = filename.split(".")[0]
                    outfile = filename_save+"_"+str(number) + "."+compression_type
                    outfile = outfolder + outfile
                    cmd = "cons_rcp.exe -s " +filename+ " -o "+outfile + " -"+compression_type +"_quality " + str(quality)
                    os.system(cmd) 
                    number = number + 1   
                else:
                    outfolder = "4288-2848_"+compression_type+"_UP_"+str(up_lim)+"_DOWN_"+str(down_lim)+"/"
                    filename_save = filename.split(".")[0]
                    # filename comes like Image_101.tiff
                    outfile = filename_save+"_"+str(number) + "."+compression_type 
                    outfile = outfolder + outfile
                    #outfile is the directory.    
                    if not os.path.exists(outfolder):
                        os.makedirs(outfolder) 
                    # If not the folder is created just create the folder to save the output files. 
                    # Compress the file for initial file size.
                    for quality in range(0,100):                      
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
  
                        
        
    def compressImage_samesize(self,compression_type,up_lim,down_lim):
        number = 0
        current_dir = os.getcwd()
        if not os.path.exists(outfolder):
            os.makedirs(outfolder)
        for filename in os.listdir(current_dir):
            if ".tiff" in filename:
                filename_save = filename.split(".")[0]
                outfile = filename_save+"_"+str(number) + "."+compression_type
                outfile = outfolder + outfile
                cmd = "cons_rcp.exe -s " +filename+ " -o "+outfile + " -"+compression_type +"_quality " + str(quality)
