import os


for filename in os.listdir('pdf_images_width_plus'):
    if filename.endswith('.png'):
        new_filename = filename[:-4] + '.jpeg'
        os.rename(os.path.join('pdf_images_width_plus', filename), os.path.join('pdf_images_width_plus', new_filename))
