import cv2
import numpy as np
import os
from datetime import datetime

# =====================================
# LOAD OUTPUT IMAGES
# =====================================

crater = cv2.imread("outputs/crater_detection.jpg")
relief = cv2.imread("outputs/relief_map.jpg")
safe = cv2.imread("outputs/safe_zone.jpg")

if crater is None:
    print("Missing crater_detection.jpg")
    exit()

if relief is None:
    print("Missing relief_map.jpg")
    exit()

if safe is None:
    print("Missing safe_zone.jpg")
    exit()

# =====================================
# REMOVE OLD PANELS
# =====================================

crater = crater[:-130, :]
relief = relief[:-120, :]
safe = safe[:-140, :]

# =====================================
# RESIZE
# =====================================

WIDTH = 800
HEIGHT = 500

crater = cv2.resize(crater, (WIDTH, HEIGHT))
relief = cv2.resize(relief, (WIDTH, HEIGHT))
safe = cv2.resize(safe, (WIDTH, HEIGHT))

# =====================================
# READ REPORT
# =====================================

image_name = "Unknown"
craters = "0"
hazard = "0"
score = "0"

report_path = "outputs/mission_report.txt"

if os.path.exists(report_path):

    with open(
        report_path,
        "r",
        encoding="utf-8"
    ) as f:

        lines = [line.strip() for line in f.readlines()]

    for i, line in enumerate(lines):

        if line == "Image:":
            image_name = lines[i + 1]

        elif line == "Detected Craters:":
            craters = lines[i + 1]

        elif line == "Hazard Coverage:":
            hazard = lines[i + 1]

        elif line == "Landing Score:":
            score = lines[i + 1]

# =====================================
# LANDING SCORE
# =====================================

try:
    score_num = int(score.split("/")[0].strip())
except:
    score_num = 0

if score_num >= 80:
    mission_status = "SAFE"
    status_color = (0, 255, 0)

elif score_num >= 50:
    mission_status = "MODERATE RISK"
    status_color = (0, 255, 255)

else:
    mission_status = "HIGH RISK"
    status_color = (0, 0, 255)

# =====================================
# LABELS ON IMAGES
# =====================================

cv2.putText(
    crater,
    "CRATER DETECTION",
    (20, 45),
    cv2.FONT_HERSHEY_SIMPLEX,
    1,
    (0, 255, 0),
    3
)

cv2.putText(
    relief,
    "TERRAIN RELIEF MAP",
    (20, 45),
    cv2.FONT_HERSHEY_SIMPLEX,
    1,
    (255, 255, 255),
    3
)

cv2.putText(
    safe,
    "SAFE LANDING ANALYSIS",
    (20, 45),
    cv2.FONT_HERSHEY_SIMPLEX,
    1,
    (0, 255, 0),
    3
)

# =====================================
# SUMMARY PANEL
# =====================================

summary = np.zeros(
    (HEIGHT, WIDTH, 3),
    dtype=np.uint8
)

cv2.putText(
    summary,
    "MISSION SUMMARY",
    (20, 50),
    cv2.FONT_HERSHEY_SIMPLEX,
    1.2,
    (255, 255, 255),
    3
)

cv2.line(
    summary,
    (20, 75),
    (760, 75),
    (0, 255, 255),
    2
)

current_time = datetime.now().strftime(
    "%d-%m-%Y  %H:%M:%S"
)

# =====================================
# OPTIONAL LOGO
# =====================================

logo_path = "assets/logo.png"

if os.path.exists(logo_path):

    logo = cv2.imread(logo_path)

    if logo is not None:

        logo = cv2.resize(
            logo,
            (120, 120)
        )

        summary[
            20:140,
            650:770
        ] = logo

# =====================================
# TELEMETRY
# =====================================

info = [

    ("Image", image_name),

    ("Detected Craters", craters),

    ("Hazard Coverage", hazard),

    ("Landing Score", score),

    ("Analysis Time", current_time)

]

y = 130

for title, value in info:

    cv2.putText(
        summary,
        f"{title}:",
        (30, y),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (255, 255, 255),
        2
    )

    cv2.putText(
        summary,
        str(value),
        (320, y),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (0, 255, 255),
        2
    )

    y += 65

# =====================================
# STATUS
# =====================================

cv2.putText(
    summary,
    "MISSION STATUS",
    (30, 450),
    cv2.FONT_HERSHEY_SIMPLEX,
    1,
    (255,255,255),
    2
)

cv2.putText(
    summary,
    mission_status,
    (380, 450),
    cv2.FONT_HERSHEY_SIMPLEX,
    1,
    status_color,
    3
)

# =====================================
# COMBINE
# =====================================

top_row = np.hstack(
    (crater, relief)
)

bottom_row = np.hstack(
    (safe, summary)
)

dashboard = np.vstack(
    (top_row, bottom_row)
)

# =====================================
# HEADER
# =====================================

header = np.zeros(
    (90, dashboard.shape[1], 3),
    dtype=np.uint8
)

cv2.putText(
    header,
    "LUNAR TERRAIN ANALYZER - MISSION DASHBOARD",
    (20, 60),
    cv2.FONT_HERSHEY_SIMPLEX,
    1.3,
    (255,255,255),
    3
)

final = np.vstack(
    (header, dashboard)
)

# =====================================
# SAVE
# =====================================

cv2.imwrite(
    "outputs/presentation_board.jpg",
    final
)

print("\nSaved:")
print("outputs/presentation_board.jpg")

# =====================================
# DISPLAY
# =====================================

cv2.namedWindow(
    "Mission Dashboard",
    cv2.WINDOW_NORMAL
)

cv2.imshow(
    "Mission Dashboard",
    final
)

cv2.waitKey(0)
cv2.destroyAllWindows()