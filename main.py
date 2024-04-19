import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

from wand.image import Image


def is_transparent(img):
    for x in range(img.width):
        for y in range(img.height):
            if img[x, y].alpha > 0:
                return False
    return True


def crop_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        with Image(filename=file_path) as img:
            north_row = int(north_entry.get())
            west_row = int(west_entry.get())
            south_row = int(south_entry.get())
            east_row = int(east_entry.get())

            crop_width = 64
            crop_height = 64

            total_steps = (img.width // crop_width) * 4
            progress_bar['maximum'] = total_steps
            progress_bar['value'] = 0

            for direction, row in zip(['north', 'west', 'south', 'east'], [north_row, west_row, south_row, east_row]):
                top = row * crop_height

                for j in range(img.width // crop_width):
                    left = j * crop_width

                    right = left + crop_width
                    bottom = top + crop_height

                    with img[left:right, top:bottom] as cropped:
                        if not is_transparent(cropped):
                            cropped.save(filename=f'{direction}_{j}.png')

                    progress_bar['value'] += 1
                    root.update_idletasks()


root = tk.Tk()
root.title("Image Cropper")

north_label = tk.Label(root, text="North Row:")
north_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
north_entry = tk.Entry(root)
north_entry.grid(row=0, column=1, padx=10, pady=5)

west_label = tk.Label(root, text="West Row:")
west_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
west_entry = tk.Entry(root)
west_entry.grid(row=1, column=1, padx=10, pady=5)

south_label = tk.Label(root, text="South Row:")
south_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
south_entry = tk.Entry(root)
south_entry.grid(row=2, column=1, padx=10, pady=5)

east_label = tk.Label(root, text="East Row:")
east_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
east_entry = tk.Entry(root)
east_entry.grid(row=3, column=1, padx=10, pady=5)

crop_button = tk.Button(root, text="Select Image and Crop", command=crop_image)
crop_button.grid(row=4, column=0, columnspan=2, pady=10)

progress_bar = ttk.Progressbar(root, orient="horizontal", mode="determinate")
progress_bar.grid(row=5, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

root.mainloop()