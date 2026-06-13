import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

from crater_detection import run_crater_detection
from relief_map import run_relief_map
from safe_zone import run_safe_zone

# =====================================
# WINDOW
# =====================================

root = tk.Tk()
root.title("LUNAR TERRAIN ANALYZER")
root.geometry("1400x850")
root.configure(bg="#111111")

selected_image = None

# =====================================
# TITLE
# =====================================

title = tk.Label(
    root,
    text="LUNAR TERRAIN ANALYZER",
    font=("Arial", 24, "bold"),
    fg="white",
    bg="#111111"
)
title.pack(pady=10)

# =====================================
# MAIN FRAME
# =====================================

main_frame = tk.Frame(root, bg="#111111")
main_frame.pack(fill="both", expand=True)

# =====================================
# LEFT PANEL
# =====================================

left_panel = tk.Frame(
    main_frame,
    bg="#1c1c1c",
    width=280
)
left_panel.pack(side="left", fill="y")
left_panel.pack_propagate(False)

# =====================================
# RIGHT PANEL
# =====================================

right_panel = tk.Frame(
    main_frame,
    bg="black"
)
right_panel.pack(side="right", fill="both", expand=True)

image_label = tk.Label(
    right_panel,
    bg="black"
)
image_label.pack(fill="both", expand=True)

# =====================================
# TELEMETRY PANEL
# =====================================

telemetry = tk.Frame(
    root,
    bg="#202020",
    height=180
)

telemetry.pack(
    fill="x",
    side="bottom"
)

telemetry.pack_propagate(False)

heading = tk.Label(
    telemetry,
    text="MISSION TELEMETRY",
    font=("Arial", 16, "bold"),
    fg="cyan",
    bg="#202020"
)

heading.pack(pady=5)

telemetry_text = tk.Label(
    telemetry,
    text=
    "Selected Image : None\n"
    "Detected Craters : -\n"
    "Average Confidence : -\n"
    "Terrain Roughness : -\n"
    "Hazard Coverage : -\n"
    "Landing Score : -\n"
    "Mission Status : -",
    justify="left",
    anchor="w",
    font=("Consolas", 11),
    fg="white",
    bg="#202020"
)

telemetry_text.pack(
    anchor="w",
    padx=20
)

# =====================================
# DISPLAY IMAGE
# =====================================

def display_image(path):

    img = Image.open(path)

    img.thumbnail((1000, 700))

    photo = ImageTk.PhotoImage(img)

    image_label.config(image=photo)

    image_label.image = photo

# =====================================
# CHOOSE IMAGE
# =====================================

def choose_image():

    global selected_image

    file_path = filedialog.askopenfilename(
        filetypes=[("Images", "*.jpg *.jpeg *.png")]
    )

    if not file_path:
        return

    selected_image = file_path

    display_image(file_path)

    telemetry_text.config(
        text=
        f"Selected Image : {os.path.basename(file_path)}\n"
        "Detected Craters : -\n"
        "Average Confidence : -\n"
        "Terrain Roughness : -\n"
        "Hazard Coverage : -\n"
        "Landing Score : -\n"
        "Mission Status : READY"
    )

# =====================================
# CRATER ANALYSIS
# =====================================

def crater_analysis():

    if not selected_image:
        messagebox.showerror(
            "Error",
            "Choose an image first"
        )
        return

    stats = run_crater_detection(
        selected_image,
        show_window=False
    )

    display_image(stats["output"])

    telemetry_text.config(
        text=
        f"Selected Image : {os.path.basename(selected_image)}\n"
        f"Detected Craters : {stats['craters']}\n"
        f"Average Confidence : {stats['avg_confidence']:.2f}\n"
        "Terrain Roughness : -\n"
        "Hazard Coverage : -\n"
        "Landing Score : -\n"
        "Mission Status : CRATER ANALYSIS COMPLETE"
    )

# =====================================
# RELIEF ANALYSIS
# =====================================

def relief_analysis():

    if not selected_image:
        messagebox.showerror(
            "Error",
            "Choose an image first"
        )
        return

    stats = run_relief_map(
        selected_image,
        show_window=False
    )

    display_image(stats["output"])

    telemetry_text.config(
        text=
        f"Selected Image : {os.path.basename(selected_image)}\n"
        "Detected Craters : -\n"
        "Average Confidence : -\n"
        f"Terrain Roughness : {stats['roughness']:.2f}\n"
        "Hazard Coverage : -\n"
        "Landing Score : -\n"
        "Mission Status : TERRAIN ANALYSIS COMPLETE"
    )

# =====================================
# SAFE LANDING
# =====================================

def safe_analysis():

    if not selected_image:
        messagebox.showerror(
            "Error",
            "Choose an image first"
        )
        return

    stats = run_safe_zone(
        selected_image,
        show_window=False
    )

    display_image(stats["output"])

    telemetry_text.config(
        text=
        f"Selected Image : {os.path.basename(selected_image)}\n"
        f"Detected Craters : {stats['craters']}\n"
        "Average Confidence : See Crater Analysis\n"
        "Terrain Roughness : See Relief Analysis\n"
        f"Hazard Coverage : {stats['hazard']:.2f}%\n"
        f"Landing Score : {stats['score']}/100\n"
        f"Mission Status : {stats['status']}"
    )

# =====================================
# BUTTONS
# =====================================

btn_choose = tk.Button(
    left_panel,
    text="Choose Image",
    font=("Arial", 14),
    width=20,
    command=choose_image
)
btn_choose.pack(pady=15)

btn_crater = tk.Button(
    left_panel,
    text="Crater Detection",
    font=("Arial", 14),
    width=20,
    command=crater_analysis
)
btn_crater.pack(pady=15)

btn_relief = tk.Button(
    left_panel,
    text="Terrain Relief",
    font=("Arial", 14),
    width=20,
    command=relief_analysis
)
btn_relief.pack(pady=15)

btn_safe = tk.Button(
    left_panel,
    text="Safe Landing",
    font=("Arial", 14),
    width=20,
    command=safe_analysis
)
btn_safe.pack(pady=15)

btn_exit = tk.Button(
    left_panel,
    text="Exit",
    font=("Arial", 14),
    width=20,
    command=root.destroy
)
btn_exit.pack(pady=50)

root.mainloop()