from PIL import Image
import os

def resize_image(file_path, output_path, size=(194, 111)):
    img = Image.open(file_path)
    img = img.resize(size)
    img.save(output_path)
    print(f"Saved resized image to {output_path}")

if __name__ == "__main__":
    resize_image("example.jpg", "resized_example.jpg")
