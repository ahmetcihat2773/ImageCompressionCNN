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
        
    def compressImage_JPEG(self,up_lim,down_lim,quality,same_quality_size,same_ssmi = False):
        """
        Compress file in jpeg format with given file_size
        """
        compression_type = "JPEG"
        compressed_num = 0
        try_num = 0
        low_quality = 1
        high_quality = 100
        self.input_folder = "4288-2848/" 
        if same_file_size:
            outfolder = "4288-2848_JPEG_samesize/"
            if not os.path.exists(outfolder):
                os.makedirs(outfolder)
            for filename in os.listdir(self.input_folder):
                try:
                    if "tiff" in filename:
                        filepath = self.input_folder + filename
                        picture = Image.open(filepath)
                        save_name = "Compressed_" + str(compressed_num) + "_"+ str(quality) + ".jpg" 
                        save_path = outfolder + save_name
                        picture.save(save_path,compression_type,optimize = True,quality = quality)
                        compressed_size = os.stat(save_path).st_size
                        while not (compressed_size> down_lim and compressed_size < up_lim):
                            try_num = try_num + 1
                            if try_num > 150:
                                os.remove(save_path)
                                break
                            if compressed_size < down_lim:
                                # If size is lower then up_lim increase the quality to make it bigger.
                                low_quality = low_quality + 1
                                picture.save(save_path,compression_type,optimize = False,quality = low_quality)
                            else:
                                if high_quality <=1:
                                    high_quality = 20
                                high_quality = high_quality - 1
                                picture.save(save_path,compression_type,optimize = False,quality = high_quality)
                            compressed_size = os.stat(save_path).st_size
                            print(compressed_size)
                    compressed_num = compressed_num + 1 
                    print(save_name)
                except:
                    "In case of error continue with the next file."
                    continue
                low_quality = 1
                high_quality = 50    
                try_num = 0        
        if same_ssmi:
            outfolder = "4288-2848_JPEG_samessmi/"
            if not os.path.exists(outfolder):
                os.makedirs(outfolder)
            for filename in os.listdir(self.input_folder):
                try:
                    if "tiff" in filename:
                        filepath = self.input_folder + filename
                        picture = Image.open(filepath)
                        save_name = "Compressed_" + str(compressed_num) + "_"+ str(quality) + ".jpg" 
                        save_path = outfolder + save_name
                        picture.save(save_path,compression_type,optimize = True,quality = quality)
                        compressed_num = compressed_num + 1
                except:
                    continue

    def compressImage_JPEG2(self):
        compressed_num = 0
        try_num = 0
        low_quality = 30
        high_quality = 100
        same_file_size = True 
        if same_file_size:
            outfolder = "4288-2848_JPEG2000_samesize/"
            if not os.path.exists(outfolder):
                os.makedirs(outfolder)
            for filename in os.listdir(self.input_folder):
                try:
                    if "tiff" in filename:
                        filepath = self.input_folder + filename
                        picture = Image.open(filepath)
                        save_name = "Compressed_" + str(compressed_num) + "_"+ str(quality) + ".jpg" 
                        save_path = outfolder + save_name
                        glymur.Jp2k(save_path)
                except:
                    continue
                break
    def compressImage_samequality(self,up_lim,down_lim,quality,same_quality,compression_type):
        number = 0
        current_dir = os.getcwd()
        try_num = 0
        for filename in os.listdir(current_dir):
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
                    low_quality = 30
                    high_quality = 100
                    if not os.path.exists(outfolder):
                        os.makedirs(outfolder)
                    try:
                        filename_save = filename.split(".")[0]
                        outfile = filename_save+"_"+str(number) + "."+compression_type 
                        outfile = outfolder + outfile 
                        cmd = "cons_rcp.exe -s " +filename+ " -o "+outfile + " -"+compression_type +"_quality " + str(quality)
                        os.system(cmd)                     
                        compressed_size = os.stat(outfile).st_size
                        while not (compressed_size> down_lim and compressed_size < up_lim):
                            try_num = try_num + 1
                            if try_num > 150:
                                os.remove(outfile)
                                break
                            if compressed_size < down_lim:
                                # If size is lower then up_lim increase the quality to make it bigger.
                                low_quality = low_quality + 5
                                cmd = "cons_rcp.exe -s " +filename+ " -o "+outfile + " -"+compression_type +"_quality " + str(low_quality)
                                os.system(cmd)
                            else:
                                if high_quality <=1:
                                    high_quality = 20
                                high_quality = high_quality - 1
                                cmd = "cons_rcp.exe -s " +filename+ " -o "+outfile + " -"+compression_type +"_quality " + str(high_quality)
                                os.system(cmd)
                            compressed_size = os.stat(outfile).st_size
                        number = number + 1 
                    except:
                        "In case of error continue with the next file."
                        continue
                low_quality = 30
                high_quality = 100  
                try_num = 0       
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