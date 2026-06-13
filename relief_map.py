import cv2
import numpy as np
import os

OUTPUT_PATH = "outputs/relief_map.jpg"


def run_relief_map(image_path, show_window=False):

    img = cv2.imread(image_path)
    if img is None:
        raise Exception(f"Image not found: {image_path}")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)

    gradient = np.sqrt(sobel_x**2 + sobel_y**2)

    gradient = cv2.normalize(gradient, None, 0, 255, cv2.NORM_MINMAX)
    gradient = gradient.astype(np.uint8)

    relief = cv2.applyColorMap(gradient, cv2.COLORMAP_TURBO)

    roughness = float(np.mean(gradient))

    panel = np.zeros((120, relief.shape[1], 3), dtype=np.uint8)

    cv2.putText(panel, "TERRAIN RELIEF MAP", (20, 35),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.putText(panel, f"Roughness: {roughness:.2f}", (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    final = np.vstack((relief, panel))

    os.makedirs("outputs", exist_ok=True)
    cv2.imwrite(OUTPUT_PATH, final)

    if show_window:
        cv2.imshow("Relief Map", final)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return {
        "roughness": roughness,
        "output": OUTPUT_PATH
    }