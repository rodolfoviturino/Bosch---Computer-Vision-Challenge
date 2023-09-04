import os

import augly.image as imaugs
# import augly.utils as utils

from math import ceil
from random import randint, random
from time import time


main_working_path = 'C:/Users/rodol/Desktop/Bosch/Extra Challenge'
path_to_background_images = f'{main_working_path}/Background Images'
path_to_smoke_images = f'{main_working_path}/Smoke Dataset'

background_images_list = os.listdir(path_to_background_images)
smoke_images_list = os.listdir(path_to_smoke_images)
number_of_synthetic_data_for_each_image = ceil(500 / len(smoke_images_list)) # I'm using 500 because I'm considering gererating 500 images with smoke inside the car for the algorithm to run porperly.

# For each smoke png image, I'll be creating other 'number_of_synthetic_data_for_each_image' synthetic images.
# Considering that I have a lot of images of the background (inside car view), then I'll not be repeating the background images that were used.
background_image_counter = 0
for smoke_image in smoke_images_list:
    smoke_image_path = f'{path_to_smoke_images}/{smoke_image}'
    print(f'\n\nProcessing image: {smoke_image_path}')
    for synthetic_creation in range(number_of_synthetic_data_for_each_image):
        try:
            print(f'loop:{synthetic_creation}')
            name_of_the_synthetic_image = time()
            path_to_save_synthetic_image_created = f'{main_working_path}/Processed Images/{name_of_the_synthetic_image}.png'

            name_of_the_background_image = f'{path_to_background_images}/{background_images_list[background_image_counter]}'
            background_image_counter += 1

            image = smoke_image_path

            should_use_blurring = randint(0, 1)
            if should_use_blurring == 1:
                print('Using Blurring')
                radius = randint(1, 5)
                image = imaugs.blur(image, radius=radius)
            else:
                pass

            should_use_brightness = randint(0, 1)
            if should_use_brightness == 1:
                print('Using Brigthness')
                factor = randint(2, 5) # 1 does not alter the image, and less than 1 gets the image darker
                image = imaugs.brightness(image, factor=factor)
            else:
                pass

            should_use_vertical_flipping = randint(0, 1)
            if should_use_vertical_flipping == 1:
                print('Using Vertical Flipping')
                image = imaugs.vflip(image)
            else:
                pass

            should_use_horizontal_flipping = randint(0, 1)
            if should_use_horizontal_flipping == 1:
                print('Using Horizontal Flipping')
                image = imaugs.hflip(image)
            else:
                pass 

            should_use_skewing = randint(0, 1)
            if should_use_skewing == 1:
                print('Using Skewing')
                image = imaugs.skew(image)
            else:
                pass 

            image.save(f'{main_working_path}/temp.png', **image.info) # Stores the image in a temporary way, so that it can be used by the overlay function.

            # opacity = randint(6, 10)/10
            x_pos = randint(0, 3)/10
            y_pos = randint(0, 3)/10
            emoji_scaling_size = randint(5, 10)/10
            overlapped_image = imaugs.functional.overlay_emoji(name_of_the_background_image, 
                                                            emoji_path=f'{main_working_path}/temp.png',
                                                            output_path=path_to_save_synthetic_image_created, 
                                                            opacity=1, 
                                                            emoji_size=emoji_scaling_size, 
                                                            x_pos=x_pos, 
                                                            y_pos=y_pos,
                                                            metadata=None, 
                                                            bboxes=None, 
                                                            bbox_format=None)
        except Exception as e:
            print(f'An exception ocurred: {e}')
    
