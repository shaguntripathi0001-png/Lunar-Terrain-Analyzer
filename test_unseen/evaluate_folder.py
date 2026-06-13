from ultralytics import YOLO
import os

model = YOLO("runs/detect/train-4/weights/best.pt")

input_folder = "test_unseen"

output_folder = "evaluation_results"

os.makedirs(output_folder, exist_ok=True)

model.predict(
    source=input_folder,
    conf=0.4,
    iou=0.3,
    save=True,
    project=output_folder,
    name="results"
)

print("Evaluation completed.")