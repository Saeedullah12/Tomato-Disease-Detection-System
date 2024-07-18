from keras.preprocessing import image
import numpy as np

def preprocess_image(img):
    img = img.resize((256, 256))
    img = img.convert('RGB')
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img /= 255.  
    return img