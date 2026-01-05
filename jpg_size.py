import os

from PIL import Image


def compress_jpeg(in_path, out_path, scale=1.0, quality=75):
    # Open the image
    img = Image.open(in_path)

    # JPEGs must be in RGB mode (removes transparency/alpha if coming from PNG)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    # Resize if scale is modified
    if scale != 1.0:
        new_size = (int(img.width * scale), int(img.height * scale))
        img = img.resize(new_size, Image.LANCZOS)

    # Save with quality and optimization
    # quality=75 is a good balance between file size and visual fidelity
    img.save(out_path, "JPEG", optimize=True, quality=quality)


path = "./data/jpg/outputs/"
compress_path = os.path.join(path, "compressed")
os.makedirs(compress_path, exist_ok=True)

for file in os.scandir(compress_path):
    os.remove(file)

for name in os.listdir(path):
    f_path = os.path.join(path, name)
    if not os.path.isfile(f_path):
        continue
    compress_jpeg(f_path, os.path.join(compress_path, name), scale=0.5)
