from PIL import Image, ImageOps
import os
from multiprocessing.pool import ThreadPool

def add_black_backgrounds(images):
     for image in images:
          add_black_background(image)

def add_black_background(image_path, output_path="./data/jpg/outputs/"):
    image_name = image_path.split("/")[-1].split(".")[0]
    # Open the original image
    image = Image.open(image_path)
    image = ImageOps.exif_transpose(image)
    
    # Calculate the desired size for a 4:5 aspect ratio
    width, height = image.size
    original_aspect_ratio = width / height
    target_aspect_ratio = 4 / 5
    
    if original_aspect_ratio > target_aspect_ratio:
        # The image is wider, so we'll match the width and add height
        new_width = width + round(width * 0.1 * 2)
        new_height = int(new_width / target_aspect_ratio)
    else:
        # The image is taller, so we'll match the height and add width
        new_height = height + round(height * 0.1 * 2)
        new_width = int(new_height * target_aspect_ratio)   

    # Create a new image with the target 4:5 aspect ratio
    new_image = Image.new(image.mode, (new_width, new_height), color=(0, 0, 0))

    # Calculate the position to paste the original image onto the new image
    paste_position = ((new_width - width) // 2, (new_height - height) // 2)
    new_image.paste(image, paste_position)

    # Save the output image
    new_image.save(output_path + f"buffed_{image_name}.jpg", quality=100)



def list_files_in_directory(directory_path):
    # List all files in the directory
    files = []
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        # Check if it's a file (and not a directory)
        if os.path.isfile(file_path):
            files.append(file_path)
    return files


def split_list(lst, n):
    k, m = divmod(len(lst), n)
    return [lst[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]



directory = "./data/jpg/inputs"
all_files = list_files_in_directory(directory)
num_procs = 8
sub_lists = split_list(all_files, num_procs)

with ThreadPool(processes=num_procs) as pool:
        # Map the square function to the numbers list
        results = pool.map(add_black_backgrounds, sub_lists)

