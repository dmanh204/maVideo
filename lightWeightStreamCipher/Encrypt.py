import cv2
import numpy as np
import lightweight as lw
import math
def xor_encrypt_decrypt(image, key):
    image_np = np.array(image)
    key_np = np.array(key, dtype=np.uint8)

    key_np = np.resize(key_np, image_np.shape)

    result = np.bitwise_xor(image_np, key_np)
    return result
#Load the image
image_path = "Lenna.png"
image = cv2.imread(image_path)

if image is None:
    print("Error: Unable to load the image.")
else:
    # Define a secret key same length as the number of pixel
    w, h, d = image.shape
    print(w)
    print(h)
    print(d)
    print(image[0][0])
    # size = math.ceil(w*h*d/32)
    # ma = lw.light(0x1234567890abcdef) # Khoi tao
    # key = []
    # for i in range(size):
        # key.extend(ma.run())
#Encrypt
    # encrypt_image = xor_encrypt_decrypt(image, key)
    # decrypt_image = xor_encrypt_decrypt(encrypt_image, key)
    # combined_image = np.hstack((image, encrypt_image, decrypt_image))
    # cv2.imshow('Original | Encrypt | Decrypt', combined_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()