import os,sys,random,shutil
from PIL import Image 

class ImageCompression():
    def __init__(self):
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



        
    def compressImage(self,up_lim,down_lim,compression_type,quality,same_file_size=False,same_ssmi = False):
        """
        Compress file in jpeg format with given file_size
        """
        compressed_num = 0
        try_num = 0
        folderpath = "4288-2848/" 
        outfolder = "4288-2848_JPEG/"
        low_quality = 1
        high_quality = 100
        if not os.path.exists(outfolder):
            os.makedirs(outfolder)
        for filename in os.listdir(folderpath):
            try:
                if compression_type == "JPEG" and same_file_size and "tiff" in filename:
                    filepath = folderpath + filename
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
                print("ERROR")
                continue
            low_quality = 1
            high_quality = 50    
            try_num = 0        
    
compressionClass = ImageCompression()
compressionClass.compressImage(up_lim = 250000,down_lim = 240000,quality= 10,compression_type= "JPEG",same_file_size=True)
