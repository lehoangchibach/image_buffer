from PIL import Image


def compress_png(in_path, out_path, scale=1.0, colors=256, use_pngquant=True):
    img = Image.open(in_path)
    if scale != 1.0:
        new_size = (int(img.width * scale), int(img.height * scale))
        img = img.resize(new_size, Image.LANCZOS)
    img = img.convert("P", palette=Image.ADAPTIVE, colors=colors)
    img.save(out_path, optimize=True)


compress_png("./sm-pam.png", "compressed.png", scale=0.5)
