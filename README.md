<img width="1918" height="1008" alt="image" src="https://github.com/user-attachments/assets/a24c3b5b-1416-426e-88c3-745f89c75257" /># 🌕 Lunar Terrain Analyzer

## Overview

Lunar Terrain Analyzer is an AI-powered lunar surface analysis system designed to assist in the evaluation of lunar terrain for potential landing missions.

The system integrates crater detection, terrain relief analysis, and safe landing zone identification into a single graphical interface, enabling users to analyze lunar images and assess landing suitability.
This project was developed to explore how computer vision and AI can assist in preliminary lunar landing-site assessment. By combining crater detection, terrain analysis, and landing-zone estimation, the system demonstrates an end-to-end workflow for lunar surface evaluation.

---

## Features

### Crater Detection

* Detects lunar craters using a YOLO-based object detection model.
* Highlights crater locations and boundaries on uploaded lunar images.

### Terrain Relief Analysis

* Generates terrain relief visualizations.
* Helps identify uneven or hazardous regions on the lunar surface.

### Safe Landing Zone Identification

* Evaluates terrain conditions and crater distribution.
* Identifies potential safe landing regions based on predefined safety criteria.

### Interactive GUI

* User-friendly graphical interface built with Tkinter.
* Image upload support.
* Zoom and pan functionality.
* Integrated analysis workflow.

---

## Technologies Used

* Python
* OpenCV
* NumPy
* YOLO
* Tkinter
* Pillow (PIL)

---

## Project Structure

```text
Lunar-Terrain-Analyzer
│
├── gui.py
├── crater_detection.py
├── relief_map.py
├── safe_zone.py
├── mission_report.py
│
├── models/
│
├── sample_images/
│
├── screenshots/
│
├── outputs/
│
├── requirements.txt
│
└── README.md
```

---

## Workflow

1. Upload a lunar surface image.
2. Detect craters using the trained YOLO model.
3. Generate terrain relief information.
4. Analyze hazards and terrain conditions.
5. Identify potential safe landing zones.
6. Display results through the graphical interface.

---

## Screenshots

### Home Screen
<img width="1915" height="1006" alt="Screenshot 2026-06-14 102124" src="https://github.com/user-attachments/assets/bf1c1463-b573-4f46-b640-14664c1d365c" />
<img width="1919" height="1007" alt="Screenshot 2026-06-14 102145" src="https://github.com/user-attachments/assets/0c73eb41-89de-497a-a2ea-d086e697eb03" />



### Crater Detection Result

<img width="1919" height="1008" alt="Screenshot 2026-06-14 102202" src="https://github.com/user-attachments/assets/e7673318-7c21-47dc-9b0c-eb9b3b73f5a7" />


### Terrain Relief Analysis

<img width="1918" height="1008" alt="Screenshot 2026-06-14 102219" src="https://github.com/user-attachments/assets/38e27802-95d1-4f60-b817-7a34482ee002" />


---

## Future Improvements

* Hazard heat map generation
* Coordinate extraction for landing zones
* Risk classification system
* Batch image processing
* Mission report generation
* DEM/Elevation data integration

---

## Applications

* Lunar mission planning
* Educational and research purposes
* Terrain analysis demonstrations
* AI-based planetary exploration studies

---

## Results

- YOLO-based crater detection on lunar imagery
- Terrain relief visualization using image processing
- Automated safe landing zone estimation
- Interactive GUI for complete analysis workflow



## Installation

```bash
git clone https://github.com/shaguntripathi0001-png/Lunar-Terrain-Analyzer.git
cd Lunar-Terrain-Analyzer
pip install -r requirements.txt
```

---

## Running the Project

```bash
python gui.py
```

---

## Author

**Shagun Tripathi**

B.Tech Computer Science (AI)

Aspiring AI Engineer | Space Technology Enthusiast
