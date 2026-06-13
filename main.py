from ultralytics import YOLO

# Load pretrained YOLO model
model = YOLO("yolov8n.pt")

# Run prediction
results = model("images/Copernicus.jpg", show=True)

print("Done")