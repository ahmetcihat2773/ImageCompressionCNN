import os,sys,random,shutil

from PIL import Image 


class ImageCompression():
    def __init__(self):
        print("IMAGE COMPRESSION IS STARTED")
    def find_resolution(self,resolution,same_file_size = False,same_ssmi = False):
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



        
    def compressImage(self,file_size,compression_type,same_file_size=False,same_ssmi = False):
        """
        Compress file in jpeg format with given file_size
        """
        file = "Image_1.tiff"
        filepath = os.path.join(os.getcwd(),file)
        
        picture = Image.open(filepath) 
        save_name = "Compressed_1.jpg"
        picture.save(save_name,"JPEG",optimize = True,quality = 10) 
        compressed_size = os.stat(save_name).st_size
        quality = 5
        last_sizes = list()
        while not (compressed_size> 24000 and compressed_size < 250000):
            if compressed_size < 250000:
                quality = quality + 1
                picture.save(save_name,"JPEG",optimize = False,quality = quality)
            else:
                if len(last_sizes) > 2:
                    if compressed_size in last_sizes:
                        quality = quality - random.randint(1,10)
                        last_sizes = list()
                        picture.save(save_name,"JPEG",optimize = False,quality = quality)
                else:
                    quality = quality - 1
                    picture.save(save_name,"JPEG",optimize = False,quality = quality)
        
            compressed_size = os.stat(save_name).st_size
            last_sizes.append(compressed_size)

    
compressionClass = ImageCompression()
