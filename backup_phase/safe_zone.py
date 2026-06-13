import os
import cv2
import numpy as np
from ultralytics import YOLO

# =====================================
# IMAGE SELECTION
# =====================================

folder = "analysis_images"

images = [
    f for f in os.listdir(folder)
    if f.lower().endswith((".jpg", ".jpeg", ".png"))
]

print("\n===================================")
print("       SAFE LANDING ANALYSIS")
print("===================================\n")

for i, img_name in enumerate(images):
    print(f"{i+1}. {img_name}")

choice = int(input("\nChoose image number: "))

image_path = os.path.join(
    folder,
    images[choice - 1]
)

# =====================================
# LOAD MODEL
# =====================================

model = YOLO("models/best.pt")

# =====================================
# LOAD IMAGE
# =====================================

img = cv2.imread(image_path)

if img is None:
    print("ERROR: Image not found")
    exit()

# =====================================
# RUN DETECTION
# =====================================

results = model.predict(
    source=image_path,
    conf=0.6,
    iou=0.3,
    save=False,
    verbose=False
)

output = img.copy()

# =====================================
# CREATE UNSAFE MASK
# =====================================

mask = np.zeros(img.shape[:2], dtype=np.uint8)

crater_count = 0

for result in results:

    boxes = result.boxes.xyxy.cpu().numpy()

    for box in boxes:

        crater_count += 1

        x1, y1, x2, y2 = map(int, box)

        # crater box
        cv2.rectangle(
            output,
            (x1, y1),
            (x2, y2),
            (0, 0, 255),
            2
        )

        padding = 20

        x1p = max(0, x1 - padding)
        y1p = max(0, y1 - padding)
        x2p = min(img.shape[1], x2 + padding)
        y2p = min(img.shape[0], y2 + padding)

        cv2.rectangle(
            mask,
            (x1p, y1p),
            (x2p, y2p),
            255,
            -1
        )

# =====================================
# SAFE REGION MAP
# =====================================

safe_mask = cv2.bitwise_not(mask)

border = 40

safe_mask[:border, :] = 0
safe_mask[-border:, :] = 0
safe_mask[:, :border] = 0
safe_mask[:, -border:] = 0

distance_map = cv2.distanceTransform(
    safe_mask,
    cv2.DIST_L2,
    5
)

normalized = cv2.normalize(
    distance_map,
    None,
    0,
    255,
    cv2.NORM_MINMAX
).astype(np.uint8)

# =====================================
# BEST LANDING ZONE
# =====================================

_, maxVal, _, maxLoc = cv2.minMaxLoc(distance_map)

best_x, best_y = maxLoc

radius = int(maxVal)
radius = min(radius, 80)

landing_score = min(100, int(maxVal * 1.5))

if radius > 15:

    cv2.circle(
        output,
        (best_x, best_y),
        radius,
        (0, 255, 0),
        3
    )

    cv2.circle(
        output,
        (best_x, best_y),
        5,
        (255, 0, 0),
        -1
    )

    cv2.putText(
        output,
        "BEST LANDING ZONE",
        (best_x - 120, best_y - radius - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2
    )

# =====================================
# HAZARD COVERAGE
# =====================================

unsafe_pixels = np.count_nonzero(mask)
total_pixels = mask.shape[0] * mask.shape[1]

hazard_percent = (
    unsafe_pixels / total_pixels
) * 100

# =====================================
# TELEMETRY PANEL
# =====================================

panel_height = 140

panel = np.zeros(
    (panel_height, output.shape[1], 3),
    dtype=np.uint8
)

cv2.putText(
    panel,
    "LUNAR SAFE LANDING ANALYSIS",
    (20, 35),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.9,
    (255, 255, 255),
    2
)

cv2.putText(
    panel,
    f"Detected Craters : {crater_count}",
    (20, 75),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.75,
    (0, 255, 255),
    2
)

cv2.putText(
    panel,
    f"Hazard Coverage : {hazard_percent:.1f}%",
    (20, 115),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.75,
    (0, 255, 255),
    2
)

cv2.putText(
    panel,
    f"Landing Score : {landing_score}/100",
    (450, 75),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.75,
    (0, 255, 0),
    2
)

cv2.putText(
    panel,
    f"Image : {os.path.basename(image_path)}",
    (450, 115),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.75,
    (255, 255, 255),
    2
)

final_image = np.vstack((output, panel))

# =====================================
# SAVE
# =====================================

os.makedirs("outputs", exist_ok=True)

cv2.imwrite(
    "outputs/safe_zone.jpg",
    final_image
)

# =====================================
# DISPLAY
# =====================================

cv2.namedWindow(
    "Safe Landing Analysis",
    cv2.WINDOW_NORMAL
)

cv2.imshow(
    "Safe Landing Analysis",
    final_image
)

print("\nSaved:")
print("outputs/safe_zone.jpg")

cv2.waitKey(0)
cv2.destroyAllWindows()