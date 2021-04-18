from ImageCompression import ImageCompression
compressionClass = ImageCompression()
#compressionClass.compressImage_JPEG(up_lim = 250000,down_lim = 240000,quality= 20,same_file_size=False,same_ssmi = True)
#compression_types = ["jxr","jp2","jpeg","bpg"]
compression_types = ["jpeg","bpg"]
quality = 60
same_quality = True
for comp_type in compression_types:
    compressionClass.compressImage_samequality(5000000,4000000,quality, same_quality, comp_type)
