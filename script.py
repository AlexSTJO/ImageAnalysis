from PIL import Image
import os
import shutil

def analyze_pixel_intensity(image_path, operator, value):
    # Create a backup of the original image
    file_name, file_extension = os.path.splitext(image_path)
    backup_path = file_name + "_backup" + file_extension

    if not os.path.exists(backup_path):
        shutil.copyfile(image_path, backup_path)
        print("Backup created at:", backup_path)
    else:
        print("Backup already exists at:", backup_path)

    image = Image.open(image_path).convert("RGB")
    pixels = image.load()

    width, height = image.size
    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]

            r = eval(str(r) + operator + value)
            g = eval(str(g) + operator + value)
            b = eval(str(b) + operator + value)

            r = max(0, min(r, 255))
            g = max(0, min(g, 255))
            b = max(0, min(b, 255))

            pixels[x, y] = (int(r), int(g), int(b))

    # Save the modified image
    image.save(image_path)
    return f"backup was created at{backup_path}"

