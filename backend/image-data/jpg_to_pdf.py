import os
from PIL import Image
import shutil
def jpgs_to_pdfs(input_folders, output_folder):
     # Prepare output directory
    if os.path.exists(output_folder):
        # If folder exists and is not empty, remove all contents
        for filename in os.listdir(output_folder):
            file_path = os.path.join(output_folder, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
    else:
        os.makedirs(output_folder)


    counter = 1
    for folder in input_folders:
        jpg_files = sorted(
            [f for f in os.listdir(folder) if f.lower().endswith(".jpg")]
        )
        image_list = []

        for jpg in jpg_files:
            path = os.path.join(folder, jpg)
            img = Image.open(path).convert("RGB").rotate(-90, expand=True)
            image_list.append(img)

        if image_list:
            output_path = os.path.join(output_folder, f"image-{counter}.pdf")
            image_list[0].save(output_path, save_all=True, append_images=image_list[1:])
            print(f"Saved: {output_path}")
            counter += 1
        else:
            print(f"No .JPG files found in: {folder}")

# === USAGE EXAMPLE ===
input_folders = [
    "images/raw-image-1",
    "images/raw-image-2",
    "images/raw-image-3",
    "images/raw-image-4",
    "images/raw-image-5",
    "images/raw-image-6",
    "images/raw-image-7",
    "images/raw-image-8",
    "images/raw-image-9",
    "images/raw-image-10",
    "images/raw-image-11",
    "images/raw-image-12",
    "images/raw-image-13",
    "images/raw-image-14",
    "images/raw-image-15",
    "images/raw-image-16",
    "images/raw-image-17",
    "images/raw-image-18",
    "images/raw-image-19",
    "images/raw-image-20",
    "images/raw-image-21",
    "images/raw-image-22",
    "images/raw-image-23",
    "images/raw-image-24",
    "images/raw-image-25",
]

output_folder = "pdfs"

jpgs_to_pdfs(input_folders, output_folder)
