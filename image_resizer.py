import os
import argparse
from PIL import Image

SUPPORTED_FORMATS = (".jpg", ".jpeg", ".png", ".bmp", ".webp")


def resize_image(input_path, output_path, size, keep_aspect=False):
    try:
        with Image.open(input_path) as img:
            if keep_aspect:
                img.thumbnail(size)
            else:
                img = img.resize(size)

            # Apply compression safely (only for JPEG)
            if output_path.lower().endswith((".jpg", ".jpeg")):
                img.save(output_path, quality=85, optimize=True)
            else:
                img.save(output_path)

            print(f"[SUCCESS] Resized: {input_path} → {output_path}")

    except Exception as e:
        print(f"[ERROR] Failed to process {input_path}: {e}")


def process_path(input_path, output_path, size, keep_aspect=False, convert=None):
    if os.path.isfile(input_path):

        if convert:
            base = os.path.splitext(output_path)[0]
            output_path = base + "." + convert.lower()

        resize_image(input_path, output_path, size, keep_aspect)

    elif os.path.isdir(input_path):

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        files = [f for f in os.listdir(input_path) if f.lower().endswith(SUPPORTED_FORMATS)]
        total = len(files)

        for index, filename in enumerate(files, start=1):
            print(f"[{index}/{total}] Processing {filename}")

            input_file = os.path.join(input_path, filename)

            if convert:
                base = os.path.splitext(filename)[0]
                output_filename = base + "." + convert.lower()
            else:
                output_filename = filename

            output_file = os.path.join(output_path, output_filename)

            resize_image(input_file, output_file, size, keep_aspect)

    else:
        print("[ERROR] Input path does not exist.")


def main():
    parser = argparse.ArgumentParser(description="Batch Image Resizer Tool")

    parser.add_argument("input", help="Input file or folder path")
    parser.add_argument("output", help="Output file or folder path")
    parser.add_argument("--width", type=int, required=True, help="Resize width")
    parser.add_argument("--height", type=int, required=True, help="Resize height")
    parser.add_argument("--keep-aspect", action="store_true", help="Maintain aspect ratio")
    parser.add_argument("--convert", help="Convert output to specific format (jpg/png/webp)")

    args = parser.parse_args()

    size = (args.width, args.height)

    process_path(
        args.input,
        args.output,
        size,
        args.keep_aspect,
        args.convert
    )


if __name__ == "__main__":
    main()