import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

from crater_detection import run_crater_detection
from relief_map import run_relief_map
from safe_zone import run_safe_zone

# ==================================================
# WINDOW
# ==================================================

root = tk.Tk()

root.title("LUNAR TERRAIN ANALYZER")
root.state("zoomed")
root.configure(bg="#111111")

selected_image = None

current_image = None
current_photo = None
zoom_factor = 1.0

# ==================================================
# TITLE
# ==================================================

title = tk.Label(
    root,
    text="LUNAR TERRAIN ANALYZER",
    font=("Arial", 24, "bold"),
    fg="white",
    bg="#111111"
)

title.pack(pady=5)

# ==================================================
# MAIN FRAME
# ==================================================

main_frame = tk.Frame(root, bg="#111111")
main_frame.pack(fill="both", expand=True)

# ==================================================
# LEFT PANEL
# ==================================================

left_panel = tk.Frame(
    main_frame,
    bg="#1c1c1c",
    width=250
)

left_panel.pack(side="left", fill="y")
left_panel.pack_propagate(False)

# ==================================================
# CENTER IMAGE PANEL
# ==================================================

center_panel = tk.Frame(
    main_frame,
    bg="black"
)

center_panel.pack(
    side="left",
    fill="both",
    expand=True
)

canvas = tk.Canvas(
    center_panel,
    bg="black",
    highlightthickness=0
)

hbar = tk.Scrollbar(
    center_panel,
    orient="horizontal",
    command=canvas.xview
)

vbar = tk.Scrollbar(
    center_panel,
    orient="vertical",
    command=canvas.yview
)

canvas.configure(
    xscrollcommand=hbar.set,
    yscrollcommand=vbar.set
)

canvas.pack(side="left", fill="both", expand=True)
vbar.pack(side="right", fill="y")
hbar.pack(side="bottom", fill="x")

# ==================================================
# RIGHT TELEMETRY PANEL
# ==================================================

right_panel = tk.Frame(
    main_frame,
    bg="#202020",
    width=350
)

right_panel.pack(side="right", fill="y")
right_panel.pack_propagate(False)

heading = tk.Label(
    right_panel,
    text="MISSION TELEMETRY",
    font=("Arial", 16, "bold"),
    fg="cyan",
    bg="#202020"
)

heading.pack(pady=15)

telemetry_text = tk.Label(
    right_panel,
    justify="left",
    anchor="nw",
    font=("Consolas", 11),
    fg="white",
    bg="#202020",
    text=
    "Selected Image : None\n\n"
    "Detected Craters : -\n\n"
    "Average Confidence : -\n\n"
    "Terrain Roughness : -\n\n"
    "Hazard Coverage : -\n\n"
    "Landing Score : -\n\n"
    "Mission Status : -"
)

telemetry_text.pack(
    anchor="nw",
    padx=15
)

# ==================================================
# IMAGE DISPLAY
# ==================================================

def display_image(path):

    global current_image
    global current_photo
    global zoom_factor

    zoom_factor = 1.0

    current_image = Image.open(path)

    update_canvas_image()

def update_canvas_image():

    global current_photo

    if current_image is None:
        return

    width = int(current_image.width * zoom_factor)
    height = int(current_image.height * zoom_factor)

    resized = current_image.resize(
        (width, height),
        Image.LANCZOS
    )

    current_photo = ImageTk.PhotoImage(resized)

    canvas.delete("all")

    canvas.create_image(
        0,
        0,
        image=current_photo,
        anchor="nw"
    )

    canvas.config(
        scrollregion=canvas.bbox("all")
    )

# ==================================================
# ZOOM
# ==================================================

def mouse_zoom(event):

    global zoom_factor

    if event.delta > 0:
        zoom_factor *= 1.1
    else:
        zoom_factor /= 1.1

    zoom_factor = max(0.2, min(zoom_factor, 8))

    update_canvas_image()

canvas.bind("<MouseWheel>", mouse_zoom)

# ==================================================
# PAN
# ==================================================

canvas.bind(
    "<ButtonPress-1>",
    lambda e: canvas.scan_mark(e.x, e.y)
)

canvas.bind(
    "<B1-Motion>",
    lambda e: canvas.scan_dragto(
        e.x,
        e.y,
        gain=1
    )
)

# ==================================================
# CHOOSE IMAGE
# ==================================================

def choose_image():

    global selected_image

    file_path = filedialog.askopenfilename(
        filetypes=[
            ("Images", "*.jpg *.jpeg *.png")
        ]
    )

    if not file_path:
        return

    selected_image = file_path

    display_image(file_path)

    telemetry_text.config(
        text=
        f"Selected Image : {os.path.basename(file_path)}\n\n"
        "Detected Craters : -\n\n"
        "Average Confidence : -\n\n"
        "Terrain Roughness : -\n\n"
        "Hazard Coverage : -\n\n"
        "Landing Score : -\n\n"
        "Mission Status : READY"
    )

# ==================================================
# CRATER ANALYSIS
# ==================================================

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
        f"Selected Image : {os.path.basename(selected_image)}\n\n"
        f"Detected Craters : {stats['craters']}\n\n"
        f"Average Confidence : {stats['avg_confidence']:.2f}\n\n"
        "Terrain Roughness : -\n\n"
        "Hazard Coverage : -\n\n"
        "Landing Score : -\n\n"
        "Mission Status : CRATER ANALYSIS COMPLETE"
    )

# ==================================================
# RELIEF ANALYSIS
# ==================================================

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
        f"Selected Image : {os.path.basename(selected_image)}\n\n"
        f"Terrain Roughness : {stats['roughness']:.2f}\n\n"
        "Mission Status : TERRAIN ANALYSIS COMPLETE"
    )

# ==================================================
# SAFE LANDING
# ==================================================

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
        f"Selected Image : {os.path.basename(selected_image)}\n\n"
        f"Detected Craters : {stats['craters']}\n\n"
        f"Hazard Coverage : {stats['hazard']:.2f}%\n\n"
        f"Landing Score : {stats['score']}/100\n\n"
        f"Safe Area Pixels : {stats['safe_area']}\n\n"
        f"Mission Status : {stats['status']}"
    )

# ==================================================
# BUTTONS
# ==================================================

buttons = [
    ("Choose Image", choose_image),
    ("Crater Detection", crater_analysis),
    ("Terrain Relief", relief_analysis),
    ("Safe Landing", safe_analysis),
    ("Exit", root.destroy)
]

for text, cmd in buttons:

    tk.Button(
        left_panel,
        text=text,
        width=20,
        font=("Arial", 14),
        command=cmd
    ).pack(pady=20)

root.mainloop()