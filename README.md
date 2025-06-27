Multi-Dental Disease Detection

Project Overview

This repository contains the Multi-Dental Disease Detection system, developed to assist dental professionals in diagnosing conditions from panoramic X-ray images. The system uses YOLOv8 for object detection and segmentation to identify dental diseases like caries, periodontal disease, and impacted teeth.this project demonstrates AI's potential in dental diagnostics with a Flask-based web interface and a Tkinter-based GUI for local use.

Features



Disease Detection: Identifies caries, periodontal issues, and impacted teeth using YOLOv8.



Object Localization: Draws bounding boxes around affected areas.



Segmentation: Segments individual teeth for detailed analysis.



Web Interface: Flask app for uploading and analyzing X-ray images.



Desktop GUI: Tkinter-based interface for local image analysis.



Real-time Processing: Optimized for efficient clinical use.

Technologies Used





Programming Language: Python 3



Libraries and Frameworks:





Ultralytics YOLOv8 for detection and segmentation



OpenCV for image processing



NumPy, Pandas for data handling



Matplotlib, Seaborn for visualization



Flask for web interface



Tkinter for desktop GUI



TensorFlow/Keras for model experimentation



Tools:





Pycharm for training



Git for version control



Overleaf for documentation



Concepts:





CNNs, Object Detection, Segmentation, Transfer Learning

Dataset

The project uses a custom dataset of panoramic X-ray images, sourced from anonymized hospital data or public datasets like Kaggle. Annotations cover caries, periodontal disease, and impacted teeth. Due to privacy and size constraints, the dataset is not included in this repository. Users must create their own dataset and data.yaml configuration file.
