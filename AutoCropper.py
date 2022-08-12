from PIL import Image
import os

"""
This file is used for cropping out transparent pixels in a sprite,
and should only ever be run on its own to make the sprite sizes tight to their design
"""
if __name__ == '__main__':
    for path in os.listdir('Images/'):
        if path.endswith('.png'):
            img = Image.open(f'Images/{path}')
            img = img.crop(img.getbbox())
            img.save(f'Images/{path}')
            img.close()
