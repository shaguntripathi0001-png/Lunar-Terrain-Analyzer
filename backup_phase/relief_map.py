import cv2
import numpy as np
import os

# ==========================================
# SHOW AVAILABLE IMAGES
# ==========================================

folder = "analysis_images"

images = [
    f for f in os.listdir(folder)
    if f.lower().endswith((".jpg", ".jpeg", ".png"))
]

if len(images) == 0:
    print("No images found inside analysis_images folder.")
    exit()

print("\n===================================")
print("      LUNAR TERRAIN ANALYZER")
print("===================================\n")

for i, img in enumerate(images):
    print(f"{i+1}. {img}")

choice = int(input("\nChoose image number: "))

image_path = os.path.join(folder, images[choice - 1])

# ==========================================
# LOAD IMAGE
# ==========================================

img = cv2.imread(image_path)

if img is None:
    print("Failed to load image.")
    exit()

# ==========================================
# GRAYSCALE
# ==========================================

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# ==========================================
# TERRAIN GRADIENT ANALYSIS
# ==========================================

sobel_x = cv2.Sobel(
    gray,
    cv2.CV_64F,
    1,
    0,
    ksize=3
)

sobel_y = cv2.Sobel(
    gray,
    cv2.CV_64F,
    0,
    1,
    ksize=3
)

gradient = np.sqrt(
    sobel_x**2 +
    sobel_y**2
)

gradient = cv2.normalize(
    gradient,
    None,
    0,
    255,
    cv2.NORM_MINMAX
)

gradient = gradient.astype(np.uint8)

# ==========================================
# RELIEF MAP COLORING
# ==========================================

relief = cv2.applyColorMap(
    gradient,
    cv2.COLORMAP_TURBO
)

# ==========================================
# INFORMATION PANEL
# ==========================================

height, width = relief.shape[:2]

panel_height = 120

panel = np.zeros(
    (panel_height, width, 3),
    dtype=np.uint8
)

cv2.putText(
    panel,
    "LUNAR TERRAIN ANALYSIS SYSTEM",
    (20, 35),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.9,
    (255, 255, 255),
    2
)

cv2.putText(
    panel,
    f"Image : {os.path.basename(image_path)}",
    (20, 70),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.7,
    (255, 255, 255),
    2
)

cv2.putText(
    panel,
    "Mode : Terrain Relief Map",
    (20, 105),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.7,
    (255, 255, 255),
    2
)

# ==========================================
# COMBINE IMAGE + PANEL
# ==========================================

final = np.vstack((relief, panel))

# ==========================================
# SAVE RESULT
# ==========================================

os.makedirs("outputs", exist_ok=True)

cv2.imwrite(
    "outputs/relief_map.jpg",
    final
)

# ==========================================
# DISPLAY
# ==========================================

cv2.imshow(
    "Terrain Relief Analysis",
    final
)

cv2.waitKey(0)
cv2.destroyAllWindows()

print("\nSaved to:")
print("outputs/relief_map.jpg")