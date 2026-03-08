import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image

SUPPORTED_FORMATS = (".jpg", ".jpeg", ".png", ".bmp", ".webp")


def resize_images(input_folder, output_folder, width, height, keep_aspect, convert):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    files = [f for f in os.listdir(input_folder) if f.lower().endswith(SUPPORTED_FORMATS)]
    total = len(files)

    progress["maximum"] = total
    progress["value"] = 0

    success_count = 0

    for index, filename in enumerate(files, start=1):
        try:
            input_path = os.path.join(input_folder, filename)

            if convert:
                base = os.path.splitext(filename)[0]
                output_filename = base + "." + convert.lower()
            else:
                output_filename = filename

            output_path = os.path.join(output_folder, output_filename)

            with Image.open(input_path) as img:
                if keep_aspect:
                    img.thumbnail((width, height))
                else:
                    img = img.resize((width, height))

                if output_path.lower().endswith((".jpg", ".jpeg")):
                    img.save(output_path, quality=85, optimize=True)
                else:
                    img.save(output_path)

            success_count += 1

        except Exception as e:
            print(f"Error processing {filename}: {e}")

        progress["value"] = index
        root.update_idletasks()

    messagebox.showinfo("Complete", f"Processed {success_count}/{total} images successfully.")


def browse_input():
    folder = filedialog.askdirectory()
    input_entry.delete(0, tk.END)
    input_entry.insert(0, folder)


def browse_output():
    folder = filedialog.askdirectory()
    output_entry.delete(0, tk.END)
    output_entry.insert(0, folder)


def start_processing():
    input_folder = input_entry.get()
    output_folder = output_entry.get()

    try:
        width = int(width_entry.get())
        height = int(height_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Width and Height must be numbers.")
        return

    keep_aspect = keep_aspect_var.get()
    convert = convert_entry.get().strip() or None

    if not os.path.isdir(input_folder):
        messagebox.showerror("Error", "Invalid input folder.")
        return

    resize_images(input_folder, output_folder, width, height, keep_aspect, convert)


# GUI Setup
root = tk.Tk()
root.title("Country Tech Image Optimizer")
root.geometry("550x350")
root.resizable(False, False)

frame = tk.Frame(root, padx=20, pady=20)
frame.pack(fill="both", expand=True)

tk.Label(frame, text="Input Folder:").grid(row=0, column=0, sticky="w")
input_entry = tk.Entry(frame, width=40)
input_entry.grid(row=1, column=0, padx=(0, 10))
tk.Button(frame, text="Browse", command=browse_input).grid(row=1, column=1)

tk.Label(frame, text="Output Folder:").grid(row=2, column=0, pady=(15, 0), sticky="w")
output_entry = tk.Entry(frame, width=40)
output_entry.grid(row=3, column=0, padx=(0, 10))
tk.Button(frame, text="Browse", command=browse_output).grid(row=3, column=1)

tk.Label(frame, text="Width:").grid(row=4, column=0, pady=(15, 0), sticky="w")
width_entry = tk.Entry(frame, width=15)
width_entry.grid(row=5, column=0, sticky="w")

tk.Label(frame, text="Height:").grid(row=4, column=1, pady=(15, 0), sticky="w")
height_entry = tk.Entry(frame, width=15)
height_entry.grid(row=5, column=1, sticky="w")

keep_aspect_var = tk.BooleanVar()
tk.Checkbutton(frame, text="Keep Aspect Ratio", variable=keep_aspect_var)\
    .grid(row=6, column=0, pady=15, sticky="w")

tk.Label(frame, text="Convert Format (jpg/png/webp optional):")\
    .grid(row=7, column=0, sticky="w")
convert_entry = tk.Entry(frame, width=15)
convert_entry.grid(row=8, column=0, sticky="w")

progress = ttk.Progressbar(frame, length=400, mode='determinate')
progress.grid(row=9, column=0, columnspan=2, pady=10)

tk.Button(frame, text="Resize Images",
          command=start_processing,
          bg="#2e7d32", fg="white", padx=20, pady=5)\
    .grid(row=10, column=0, columnspan=2, pady=10)

root.mainloop()
