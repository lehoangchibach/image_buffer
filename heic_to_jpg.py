import os
from multiprocessing.pool import ThreadPool

from PIL import Image
from pillow_heif import register_heif_opener

register_heif_opener()


def list_files_in_directory(directory_path):
    files = []
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            files.append(file_path)
    return files


def convert_heics_to_jpg(heic_paths):
    for file in heic_paths:
        # Note: Ensure the output directory exists
        convert_heic_to_jpg(file, "./data/heic/outputs/")


def convert_heic_to_jpg(heic_path, output_path="data/heic/outputs/"):
    image_name = os.path.basename(heic_path).split(".")[0]
    output_filename = os.path.join(output_path, f"heic_{image_name}.jpg")

    image = Image.open(heic_path)

    # 1. Capture the EXIF metadata
    exif_data = image.info.get("exif")

    # Convert to RGB
    image = image.convert("RGB")

    # 2. Save with EXIF data included
    if exif_data:
        image.save(output_filename, "JPEG", quality=100, exif=exif_data)
    else:
        image.save(output_filename, "JPEG", quality=100)

    # 3. Copy filesystem timestamps (Access and Modification time)
    st = os.stat(heic_path)
    os.utime(output_filename, (st.st_atime, st.st_mtime))


def split_list(lst, n):
    if n == 0:
        return [lst]
    k, m = divmod(len(lst), n)
    return [lst[i * k + min(i, m) : (i + 1) * k + min(i + 1, m)] for i in range(n)]


# Example usage
directory = "./data/heic/inputs"
output_dir = "./data/heic/outputs/"

# Ensure output directory exists before processing
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

all_files = list_files_in_directory(directory)
num_procs = 8
sub_lists = split_list(all_files, num_procs)

print(f"Processing {len(all_files)} files...")
with ThreadPool(processes=num_procs) as pool:
    pool.map(convert_heics_to_jpg, sub_lists)
print("Done!")
