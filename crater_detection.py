import cv2
import numpy as np
import os
from ultralytics import YOLO

MODEL_PATH = "models/best.pt"
OUTPUT_PATH = "outputs/crater_detection.jpg"

model = YOLO(MODEL_PATH)


def run_crater_detection(image_path, show_window=False):

    img = cv2.imread(image_path)
    if img is None:
        raise Exception(f"Image not found: {image_path}")

    results = model.predict(
        source=image_path,
        conf=0.4,
        iou=0.3,
        save=False,
        verbose=False
    )

    output = img.copy()

    crater_count = 0
    confidences = []

    for result in results:
        boxes = result.boxes.xyxy.cpu().numpy()
        confs = result.boxes.conf.cpu().numpy()

        for box, conf in zip(boxes, confs):
            crater_count += 1
            confidences.append(float(conf))

            x1, y1, x2, y2 = map(int, box)

            cv2.rectangle(output, (x1, y1), (x2, y2), (0, 255, 0), 2)

            cv2.putText(
                output,
                f"{conf:.2f}",
                (x1, max(y1 - 5, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 255),
                2
            )

    avg_conf = float(np.mean(confidences)) if confidences else 0.0

    panel = np.zeros((130, output.shape[1], 3), dtype=np.uint8)

    cv2.putText(panel, "CRATER DETECTION", (20, 35),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.putText(panel, f"Craters: {crater_count}", (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.putText(panel, f"Avg Conf: {avg_conf:.2f}", (300, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    final = np.vstack((output, panel))

    os.makedirs("outputs", exist_ok=True)
    cv2.imwrite(OUTPUT_PATH, final)

    if show_window:
        cv2.imshow("Crater Detection", final)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return {
        "craters": crater_count,
        "avg_confidence": avg_conf,
        "output": OUTPUT_PATH
    }