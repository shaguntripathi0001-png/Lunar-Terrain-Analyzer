from PIL import Image
import os

input_folder = "dataset/images/train"

for filename in os.listdir(input_folder):

    if filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):

        img_path = os.path.join(input_folder, filename)

        try:
            img = Image.open(img_path).convert("RGB")

            new_name = os.path.splitext(filename)[0] + ".jpg"

            save_path = os.path.join(input_folder, new_name)

            img.save(save_path, "JPEG")

            print(f"Converted: {filename} -> {new_name}")

        except Exception as e:
            print(f"FAILED: {filename} | {e}")