
import imagecodecs
data = open('Image_1_0.jxr', 'rb').read()
im = imagecodecs.jxr_decode(data)
#im = imageio.imread('Image_1_0.jxr',format='JXR')
