import cv2
import numpy as np
import os
from ultralytics import YOLO

# =====================================
# IMAGE SELECTION
# =====================================

folder = "analysis_images"

if not os.path.exists(folder):
    print(f"Folder not found: {folder}")
    exit()

images = [
    f for f in os.listdir(folder)
    if f.lower().endswith((".jpg", ".jpeg", ".png"))
]

if len(images) == 0:
    print("No images found in analysis_images")
    exit()

print("\n===================================")
print("       CRATER DETECTION MODE")
print("===================================\n")

for i, img_name in enumerate(images):
    print(f"{i+1}. {img_name}")

choice = int(input("\nChoose image number: "))

if choice < 1 or choice > len(images):
    print("Invalid selection")
    exit()

image_path = os.path.join(folder, images[choice - 1])

# =====================================
# LOAD MODEL
# =====================================

model = YOLO("models/best.pt")

# =====================================
# LOAD IMAGE
# =====================================

img = cv2.imread(image_path)

if img is None:
    print("Failed to load image")
    exit()

# =====================================
# PREDICTION
# =====================================

results = model.predict(
    source=image_path,
    conf=0.4,
    iou=0.3,
    save=False,
    verbose=False
)

output = img.copy()

crater_count = 0
confidence_list = []

# =====================================
# DRAW DETECTIONS
# =====================================

for result in results:

    boxes = result.boxes.xyxy.cpu().numpy()
    confs = result.boxes.conf.cpu().numpy()

    print(f"Detections: {len(boxes)}")

    for box, conf in zip(boxes, confs):

        crater_count += 1
        confidence_list.append(float(conf))

        x1, y1, x2, y2 = map(int, box)

        # Strong visible box
        cv2.rectangle(
            output,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            4
        )

        # Detection label
        cv2.putText(
            output,
            f"{conf:.2f}",
            (x1, max(y1 - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2
        )

# =====================================
# STATS
# =====================================

avg_conf = 0

if len(confidence_list) > 0:
    avg_conf = sum(confidence_list) / len(confidence_list)

# =====================================
# TELEMETRY PANEL
# =====================================

panel_height = 130

panel = np.zeros(
    (panel_height, output.shape[1], 3),
    dtype=np.uint8
)

cv2.putText(
    panel,
    "LUNAR CRATER DETECTION SYSTEM",
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
    f"Craters Detected : {crater_count}",
    (20, 105),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.7,
    (0, 255, 0),
    2
)

cv2.putText(
    panel,
    f"Average Confidence : {avg_conf:.2f}",
    (400, 105),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.7,
    (0, 255, 255),
    2
)

# =====================================
# COMBINE
# =====================================

final = np.vstack((output, panel))

# =====================================
# SAVE
# =====================================

os.makedirs("outputs", exist_ok=True)

save_path = os.path.join(
    "outputs",
    "crater_detection.jpg"
)

cv2.imwrite(save_path, final)

print("\nSaved:")
print(save_path)

# =====================================
# DISPLAY
# =====================================

cv2.namedWindow(
    "Lunar Crater Detection",
    cv2.WINDOW_NORMAL
)

cv2.setWindowProperty(
    "Lunar Crater Detection",
    cv2.WND_PROP_FULLSCREEN,
    cv2.WINDOW_FULLSCREEN
)

cv2.imshow(
    "Lunar Crater Detection",
    final
)

cv2.waitKey(0)
cv2.destroyAllWindows()