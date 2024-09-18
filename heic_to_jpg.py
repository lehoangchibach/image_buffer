from PIL import Image
from pillow_heif import register_heif_opener
import os
from multiprocessing.pool import ThreadPool
register_heif_opener()


def list_files_in_directory(directory_path):
    # List all files in the directory
    files = []
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        # Check if it's a file (and not a directory)
        if os.path.isfile(file_path):
            files.append(file_path)
    return files


def convert_heics_to_jpg(heic_paths):
    for file in heic_paths:
        convert_heic_to_jpg(file, "data/heic/outputs/")


def convert_heic_to_jpg(heic_path, output_path="data/heic/outputs/"):
    image_name = heic_path.split("\\")[-1].split(".")[0]
    image = Image.open(heic_path)
    
    # Convert the image to RGB (since HEIC might be in different color formats)
    image = image.convert("RGB")
    
    # Save the image as a JPG file
    image.save(output_path + f"heic_{image_name}.jpg", "JPEG", quality=100)


def split_list(lst, n):
    k, m = divmod(len(lst), n)
    return [lst[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]



# Example usage
directory = "data/heic/inputs"
all_files = list_files_in_directory(directory)
num_procs = 8
sub_lists = split_list(all_files, num_procs)

with ThreadPool(processes=num_procs) as pool:
        # Map the square function to the numbers list
        results = pool.map(convert_heics_to_jpg, sub_lists)

