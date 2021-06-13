from ImageCompression import ImageCompression

import numpy as np

compressionClass = ImageCompression()

#compressionClass.compressImage_JPEG(up_lim = 250000,down_lim = 240000,quality= 20,same_file_size=False,same_ssmi = True)

#compression_types = ["jxr","jp2","jpeg","bpg"]

compression_types = ["jpeg"]

expected_quality = 0.9

start_size = 1024000

stop_size = 10*start_size

step_size = 1024*200

# range is 200kbyte

same_quality = True

for comp_type in compression_types:

    if same_quality == True:

        compressionClass.same_quality_jxr(expected_quality)

    else:

        for file_size in range(start_size,stop_size,step_size):

            compressionClass.compressImage_samesize(file_size+step_size,file_size,comp_type)

