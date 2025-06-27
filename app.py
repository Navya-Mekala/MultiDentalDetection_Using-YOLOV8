import os
from flask import Flask, render_template, request, redirect, flash
from werkzeug.utils import secure_filename
from ultralytics import YOLO
import cv2
import pandas as pd

app = Flask(__name__)
app.secret_key = "dental_app_secret"
app.config["UPLOAD_FOLDER"] = "static/uploads"
app.config["RESULT_FOLDER"] = "static/results"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs(app.config["RESULT_FOLDER"], exist_ok=True)

# Load YOLO model
model = YOLO("d:/navya/Downloads/Code_Files_Batch_17 (1)/dental_/runs/detect/train9")

# Allowed extensions for upload
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "bmp"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_disease_suggestions(diseases):
    suggestions = {
        "Caries": "Consider fluoride treatments or fillings and maintain oral hygiene.",
        "Crown": "Visit your dentist for proper crown placement or replacement if necessary.",
        "Filling": "Check the condition of fillings periodically and avoid chewing hard foods.",
        "Implant": "Ensure regular check-ups for implants and follow post-surgery care instructions.",
        "Malaligned": "Consult an orthodontist for braces or aligners to correct alignment.",
        "Mandibular Canal": "Seek professional evaluation if pain or numbness is present.",
        "Missing teeth": "Discuss options like bridges, implants, or dentures with your dentist.",
        "Periapical lesion": "Promptly consult a dentist to prevent the spread of infection.",
        "Retained root": "Consider surgical removal to prevent infections or complications.",
        "Root Canal Treatment": "Ensure regular follow-ups to check the treated tooth's health.",
        "Root Piece": "Consult a dentist to evaluate the need for extraction or treatment.",
        "croen": "Visit a dentist to assess the crown's fit and condition.",
        "impacted tooth": "Seek an oral surgeon’s advice for possible extraction or treatment.",
        "maxillary sinus": "Consult a dentist or ENT specialist if discomfort or sinusitis symptoms occur.",
    }
    return "; ".join(suggestions.get(disease, "Consult a dentist for further advice.") for disease in diseases)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_image():
    if "file" not in request.files:
        flash("No file part")
        return redirect(request.url)
    file = request.files["file"]
    if file.filename == "":
        flash("No selected file")
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)
        result_path, diseases_detected = detect_disease(filepath, filename)
        suggestions = get_disease_suggestions(diseases_detected)
        return render_template("index.html", uploaded_image=filepath, result_image=result_path,
                               diseases=diseases_detected, suggestions=suggestions)
    else:
        flash("Allowed file types are png, jpg, jpeg, bmp")
        return redirect(request.url)


def detect_disease(image_path, filename):
    image = cv2.imread(image_path)
    results = model(source=image)
    res_plotted = results[0].plot()
    result_filename = f"result_{filename}"
    result_path = os.path.join(app.config["RESULT_FOLDER"], result_filename)
    cv2.imwrite(result_path, res_plotted)

    # Extract detected classes
    if results[0].boxes is not None:
        # Extract class indices from the YOLO output
        class_indices = results[0].boxes.cls.cpu().numpy()
        # Convert class indices to class names using the model's class names
        diseases_detected = [model.names[int(idx)] for idx in class_indices]
    else:
        diseases_detected = []

    return result_path, diseases_detected



@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    if request.method == "POST":
        name = request.form.get("name")
        feedback_text = request.form.get("feedback")
        if not name or not feedback_text:
            flash("Please fill in both fields")
            return redirect(request.url)

        feedback_data = {"Name": [name], "Feedback": [feedback_text]}
        feedback_df = pd.DataFrame(feedback_data)
        feedback_file = "feedback.xlsx"
        try:
            if os.path.exists(feedback_file):
                existing_df = pd.read_excel(feedback_file)
                feedback_df = pd.concat([existing_df, feedback_df], ignore_index=True)
            feedback_df.to_excel(feedback_file, index=False)
            flash("Feedback submitted successfully!")
        except Exception as e:
            flash(f"Failed to save feedback: {e}")
        return redirect(request.url)
    return render_template("feedback.html")


if __name__ == "__main__":
    app.run(debug=True)
