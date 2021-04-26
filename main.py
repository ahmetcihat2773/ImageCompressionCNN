from ImageCompression import ImageCompression
compressionClass = ImageCompression()
#compressionClass.compressImage_JPEG(up_lim = 250000,down_lim = 240000,quality= 20,same_file_size=False,same_ssmi = True)
#compression_types = ["jxr","jp2","jpeg","bpg"]
compression_types = ["jxr"]
start_size = 1024000
stop_size = 10*start_size
step_size = 1024*200
# range is 200kbyte
quality = 60
same_quality = False
for comp_type in compression_types:
    for file_size in range(start_size,stop_size,step_size):
        compressionClass.compressImage_samequality(file_size+step_size,file_size,quality, same_quality, comp_type)
