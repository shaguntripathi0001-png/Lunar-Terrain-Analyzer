import cv2
import numpy as np
import os
from ultralytics import YOLO

MODEL_PATH = "models/best.pt"
OUTPUT_PATH = "outputs/safe_zone.jpg"

model = YOLO(MODEL_PATH)


def run_safe_zone(image_path, show_window=False):

    img = cv2.imread(image_path)

    if img is None:
        raise Exception(f"Image not found: {image_path}")

    h, w = img.shape[:2]

    # =====================================
    # CRATER DETECTION
    # =====================================

    results = model.predict(
        source=image_path,
        conf=0.6,
        iou=0.3,
        save=False,
        verbose=False
    )

    output = img.copy()

    crater_mask = np.zeros((h, w), dtype=np.uint8)

    crater_count = 0

    for result in results:

        boxes = result.boxes.xyxy.cpu().numpy()

        for box in boxes:

            crater_count += 1

            x1, y1, x2, y2 = map(int, box)

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
            x2p = min(w, x2 + padding)
            y2p = min(h, y2 + padding)

            cv2.rectangle(
                crater_mask,
                (x1p, y1p),
                (x2p, y2p),
                255,
                -1
            )

    # =====================================
    # SHADOW DETECTION
    # =====================================

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )

    shadow_mask = np.zeros_like(gray)

    shadow_mask[gray < 35] = 255

    # =====================================
    # TERRAIN ROUGHNESS
    # =====================================

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
        sobel_x ** 2 +
        sobel_y ** 2
    )

    gradient = cv2.normalize(
        gradient,
        None,
        0,
        255,
        cv2.NORM_MINMAX
    )

    gradient = gradient.astype(np.uint8)

    roughness_mask = np.zeros_like(gray)

    roughness_mask[gradient > 45] = 255

    # =====================================
    # COMBINED HAZARD MAP
    # =====================================

    hazard_mask = cv2.bitwise_or(
        crater_mask,
        shadow_mask
    )

    hazard_mask = cv2.bitwise_or(
        hazard_mask,
        roughness_mask
    )

    safe_mask = cv2.bitwise_not(
        hazard_mask
    )

    border = 40

    safe_mask[:border, :] = 0
    safe_mask[-border:, :] = 0
    safe_mask[:, :border] = 0
    safe_mask[:, -border:] = 0

    # =====================================
    # SAFE REGION SEARCH
    # =====================================

    num_labels, labels, stats, centroids = \
        cv2.connectedComponentsWithStats(
            safe_mask
        )

    best_area = 0
    best_label = -1

    for i in range(1, num_labels):

        area = stats[i, cv2.CC_STAT_AREA]

        if area > best_area:
            best_area = area
            best_label = i

    # =====================================
    # LANDING DECISION
    # =====================================

    landing_possible = False

    MIN_SAFE_AREA = 5000

    if best_area > MIN_SAFE_AREA:

        landing_possible = True

        cx, cy = centroids[best_label]

        cx = int(cx)
        cy = int(cy)

        region_mask = np.uint8(
            labels == best_label
        ) * 255

        contours, _ = cv2.findContours(
            region_mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        cv2.drawContours(
            output,
            contours,
            -1,
            (0, 255, 0),
            3
        )

        cv2.circle(
            output,
            (cx, cy),
            6,
            (255, 0, 0),
            -1
        )

        cv2.putText(
            output,
            "RECOMMENDED LANDING SITE",
            (cx - 120, cy - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

    else:

        cv2.putText(
            output,
            "NO SAFE LANDING SITE FOUND",
            (40, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            3
        )

        cv2.putText(
            output,
            "LANDING ABORT RECOMMENDED",
            (40, 130),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2
        )

    # =====================================
    # METRICS
    # =====================================

    hazard_percent = (
        np.count_nonzero(hazard_mask)
        / hazard_mask.size
    ) * 100

    if landing_possible:

        area_score = min(
            100,
            int(best_area / 100)
        )

        hazard_score = max(
            0,
            int(100 - hazard_percent)
        )

        landing_score = int(
            0.6 * area_score +
            0.4 * hazard_score
        )

    else:

        landing_score = 0

    status = (
        "SAFE"
        if landing_possible
        else
        "ABORT"
    )

    # =====================================
    # TELEMETRY PANEL
    # =====================================

    panel = np.zeros(
        (160, w, 3),
        dtype=np.uint8
    )

    cv2.putText(
        panel,
        "LUNAR LANDING SITE ANALYSIS",
        (20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (255, 255, 255),
        2
    )

    cv2.putText(
        panel,
        f"Craters : {crater_count}",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        (0, 255, 255),
        2
    )

    cv2.putText(
        panel,
        f"Hazard Coverage : {hazard_percent:.1f}%",
        (20, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        (0, 255, 255),
        2
    )

    cv2.putText(
        panel,
        f"Landing Score : {landing_score}/100",
        (450, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        (0, 255, 0) if landing_possible else (0, 0, 255),
        2
    )

    cv2.putText(
        panel,
        f"Status : {status}",
        (450, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        (0, 255, 0) if landing_possible else (0, 0, 255),
        2
    )

    final = np.vstack(
        (output, panel)
    )

    os.makedirs(
        "outputs",
        exist_ok=True
    )

    cv2.imwrite(
        OUTPUT_PATH,
        final
    )

    if show_window:
        cv2.imshow(
            "Safe Landing Analysis",
            final
        )
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return {
        "craters": crater_count,
        "hazard": round(hazard_percent, 2),
        "score": landing_score,
        "status": status,
        "safe_area": int(best_area),
        "output": OUTPUT_PATH
    }