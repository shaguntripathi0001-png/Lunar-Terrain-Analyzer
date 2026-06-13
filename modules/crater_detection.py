import cv2
import numpy as np
import os
from ultralytics import YOLO

MODEL_PATH = "models/best.pt"
OUTPUT_PATH = "outputs/crater_detection.jpg"


def run_crater_detection(image_path, show_window=True):

    model = YOLO(MODEL_PATH)

    img = cv2.imread(image_path)

    if img is None:
        raise Exception(f"Failed to load image: {image_path}")

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

    for result in results:

        boxes = result.boxes.xyxy.cpu().numpy()
        confs = result.boxes.conf.cpu().numpy()

        for box, conf in zip(boxes, confs):

            crater_count += 1
            confidence_list.append(float(conf))

            x1, y1, x2, y2 = map(int, box)

            cv2.rectangle(
                output,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                4
            )

            cv2.putText(
                output,
                f"{conf:.2f}",
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 255),
                2
            )

    avg_conf = 0

    if len(confidence_list) > 0:
        avg_conf = sum(confidence_list) / len(confidence_list)

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

    final = np.vstack((output, panel))

    os.makedirs("outputs", exist_ok=True)

    cv2.imwrite(
        OUTPUT_PATH,
        final
    )

    if show_window:

        cv2.namedWindow(
            "Lunar Crater Detection",
            cv2.WINDOW_NORMAL
        )

        cv2.imshow(
            "Lunar Crater Detection",
            final
        )

        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return {
        "craters": crater_count,
        "avg_confidence": round(avg_conf, 2),
        "output": OUTPUT_PATH
    }


if __name__ == "__main__":

    folder = "analysis_images"

    images = [
        f for f in os.listdir(folder)
        if f.lower().endswith(
            (".jpg", ".jpeg", ".png")
        )
    ]

    print("\nAvailable Images:\n")

    for i, img in enumerate(images):
        print(f"{i+1}. {img}")

    choice = int(input("\nChoose image number: "))

    image_path = os.path.join(
        folder,
        images[choice - 1]
    )

    stats = run_crater_detection(
        image_path,
        show_window=True
    )

    print(stats)