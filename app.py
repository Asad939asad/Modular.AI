from flask import Flask, render_template, request
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from PIL import Image


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/module/DoctorBot", methods=["GET", "POST"])
def doctorbot():
    response = ""
    if request.method == "POST":
        user_query = request.form.get("query")

        # 🔧 Replace this with your actual LLM call
        response = f"""DoctorBot says: You asked - '{user_query}'. (Sure, I can help you with that. Here are some steps you can follow to get some relief from your headache:

1. Try taking some over-the-counter pain medication, such as ibuprofen, to help relieve your headache pain.

2. If your headache pain persists, try taking some over-the-counter pain medication, such as ibuprofen, to help relieve your headache pain.

3. If your headache pain persists, try taking some over-the-counter pain medication, such as ibuprofen, to help relieve your headache pain."""
    return render_template("DoctorBot.html", response=response)


@app.route("/module/<module_name>")
def module_page(module_name):
    return f"<h1>{module_name.replace('-', ' ').title()} Page Coming Soon</h1>"


@app.route("/module/PostureCorrector")
def posture_corrector():
    return render_template("posture.html")

app.config["UPLOAD_FOLDER"] = "./static/uploads"

# Create upload folder if not exists
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

import os

UPLOAD_FOLDER = os.path.join("static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/module/ECGAnalyzer", methods=["GET", "POST"])
def ecg_analyzer():
    image_filename = None
    label = None

    if request.method == "POST":
        file = request.files.get("ecg_image")
        if file:
            image_filename = file.filename
            file.save(os.path.join(UPLOAD_FOLDER, image_filename))

            # Replace this with your model inference logic
            label = "Abnormal Heart Beat"

    return render_template(
        "ecg_analyzer.html", image_filename=image_filename, label=label
    )


# Dummy model function (replace this with your actual model)
def get_prescribed_drugs(symptoms):
    # Example mock logic
    return ["1. amlopres-at tablet — Matched Use: hypertension (high blood pressure) (Score: 0.5083)", "2. aquazide 12.5 tablet — Matched Use: hypertension (high blood pressure) (Score: 0.5083)","3. amlovas 5 tablet — Matched Use: hypertension (high blood pressure) (Score: 0.5083)"]


@app.route("/module/Drugs", methods=["GET", "POST"])
def index():
    drugs = []
    if request.method == "POST":
        symptoms = request.form["symptoms"]
        drugs = get_prescribed_drugs(symptoms)
    return render_template("drug_prescriber.html", drugs=drugs)


@app.route("/module/VLM", methods=["GET", "POST"])
def analyze():
    if request.method == "POST":
        file = request.files["radiology_image"]
        if file:
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

            # Generate a dummy description for now
            description = (
                "Skeleton image."
            )

            return render_template(
                "radiology_vlm.html",
                image_filename=file.filename,
                description=description,
            )

    return render_template("radiology_vlm.html")


@app.route("/module/description", methods=["GET", "POST"])
def drug_description():
    if request.method == "POST":
        file = request.files["drug_image"]
        if file:
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

            # Placeholder: Replace this with your model's actual output
            description = (
                """Azax500r Film Tablet (a substitute for a drug like "Azee 250 Tablet") is an antibiotic used to treat bacterial infections. It belongs to a class of drugs called Macrolides. While taking this medicine, some common side effects you might experience include vomiting, nausea, abdominal pain, or diarrhea.
                   This medication is not habit-forming. If you're unable to obtain Azax500r, some alternatives your doctor might suggest include medications similar to Azicip 250 Tablet, Azikem 250mg Tablet, Fitzee 250 Tablet, Azi Q 250mg Tablet, or Azax 250 Tablet. Always consult your doctor or pharmacist before switching medications."""

            )

            return render_template(
                "description_generation.html",
                image_filename=file.filename,
                description=description,
            )

    return render_template("description_generation.html")


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')
