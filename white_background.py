import io
import os
import shutil
from pathlib import Path

from PIL import Image
from rembg import new_session, remove


def process_images(input_folder, output_folder):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Supported extensions
    extensions = (".jpg", ".jpeg", ".JPG", ".JPEG")
    # session = new_session("u2netp")  # isnet-general-use OR remove line
    session = new_session("u2netp")

    for filename in os.listdir(input_folder):
        if filename.endswith(extensions):
            input_path = os.path.join(input_folder, filename)

            # Generate output filename (changing extension to .jpg)
            output_path = os.path.join(
                output_folder, f"{Path(filename).stem}_white_bg.jpg"
            )

            print(f"Processing: {filename}...")

            try:
                # Open the image
                with open(input_path, "rb") as i:
                    input_image = i.read()

                    # Remove background (returns image with transparency)
                    # no_bg_image = remove(input_image)

                    no_bg_image = remove(
                        input_image,
                        alpha_matting=True,
                        alpha_matting_foreground_threshold=240,
                        alpha_matting_background_threshold=10,
                        alpha_matting_erode_size=10,
                        session=session,
                    )

                    # Load into PIL to manipulate background color
                    img = Image.open(io.BytesIO(no_bg_image)).convert("RGBA")

                    # Create a white background
                    white_bg = Image.new("RGBA", img.size, "WHITE")

                    # Paste the foreground onto the white background
                    white_bg.paste(img, (0, 0), img)

                    # Convert to RGB (required for JPG) and save
                    final_img = white_bg.convert("RGB")
                    final_img.save(output_path, "JPEG", quality=95)

            except Exception as e:
                print(f"Failed to process {filename}: {e}")


# Usage
input_dir = "./data/jpg/inputs"
output_dir = "./data/jpg/outputs/"

shutil.rmtree(output_dir)
os.makedirs(output_dir, exist_ok=True)

process_images(input_dir, output_dir)
