import os
from iris_rubber_sheet import process_img

root_folders = os.listdir("dataset")

inner_folders = ["1L", "1R", "2L", "2R"]

for folder in root_folders:
    if int(folder) < 99:
        continue
    for name in inner_folders:
        input_images = os.listdir(f"dataset/{folder}/{name}")
        os.makedirs(f"out/{folder}/{name}/iris", exist_ok=True)
        os.makedirs(f"out/{folder}/{name}/rubber_sheets", exist_ok=True)
        for image in input_images:
            image_path = f"dataset/{folder}/{name}/{image}"
            print(image_path)
            process_img(
                image_path,
                f"out/{folder}/{name}/iris/iris_{image}",
                f"out/{folder}/{name}/rubber_sheets/rs_{image}",
            )
