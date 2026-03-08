from PIL import Image
import os
import argparse
import sys


def resize_image(input_path: str, output_path: str, width: int, height: int) -> None:
    """
    Resize a single image and save it to output path.
    """
    try:
        with Image.open(input_path) as img:
            resized = img.resize((width, height))
            resized.save(output_path)
            print(f"[SUCCESS] Resized: {input_path} → {output_path}")
    except Exception as e:
        print(f"[ERROR] Failed to process {input_path}: {e}")


def resize_folder(input_folder: str, output_folder: str, width: int, height: int) -> None:
    """
    Resize all images in a folder.
    """
    if not os.path.exists(input_folder):
        print(f"[ERROR] Input folder '{input_folder}' not found.")
        sys.exit(1)

    os.makedirs(output_folder, exist_ok=True)

    supported_formats = (".jpg", ".jpeg", ".png", ".webp")

    processed = 0

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(supported_formats):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            resize_image(input_path, output_path, width, height)
            processed += 1

    print(f"[INFO] Total images processed: {processed}")


def main():
    parser = argparse.ArgumentParser(
        description="Bulk image resizing tool for web and e-commerce optimization."
    )
    parser.add_argument("input", help="Input image file OR folder")
    parser.add_argument("output", help="Output image file OR folder")
    parser.add_argument("--width", type=int, default=800, help="Resize width (default: 800)")
    parser.add_argument("--height", type=int, default=600, help="Resize height (default: 600)")

    args = parser.parse_args()

    if os.path.isdir(args.input):
        resize_folder(args.input, args.output, args.width, args.height)
    else:
        resize_image(args.input, args.output, args.width, args.height)


if __name__ == "__main__":
    main()
