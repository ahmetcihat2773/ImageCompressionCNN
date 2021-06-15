from ImageCompression import ImageCompression

import numpy as np

compressionClass = ImageCompression()

#compressionClass.compressImage_JPEG(up_lim = 250000,down_lim = 240000,quality= 20,same_file_size=False,same_ssmi = True)

#compression_types = ["jxr","jp2","jpeg","bpg"]

compression_types = ["jpeg","jpg2"]

expected_quality = [0.9]

start_size = 3024000

stop_size = 10*start_size

step_size = 1024*200

# 1024 byte 1kbyte and 5kbyte step size.

same_quality = False

for comp_type in compression_types:

    if same_quality == True:
        for expected_val in expected_quality:
            compressionClass.same_quality_jxr(expected_val)

    else:
        if comp_type == "jpeg":
            compressionClass.compressImage_samesize_jpeg(start_size+step_size,start_size-step_size)
        elif comp_type = "jpg2":
            compressionClass.compressImage_samesize_jpeg2000(start_size+step_size,start_size-step_size,"jpg2")

        else:
            compressionClass.samesize_jxr(start_size+step_size,start_size-step_size)


        

