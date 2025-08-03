from flask import Flask, render_template, request, Response
from ultralytics import YOLO
import pandas as pd
import os
import cv2
import uuid

app = Flask(__name__)


MODEL_PATH = "static/models/best.pt"
CSV_PATH = "static/data/artwork_descriptions_first25.csv"
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


model = YOLO(MODEL_PATH)
csv_data = pd.read_csv(CSV_PATH)


@app.route("/", methods=["GET", "POST"])

def index():
    result = None
    suggestions = []

    if request.method == "POST":
        file = request.files["image"]
        if file:
            filename = file.filename
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            try:
                results = model(filepath)
                if results[0].boxes.cls.numel() == 0:
                    result = {"error": "Model görselde tablo bulamadı."}
                    return render_template("index.html", result=result)

                class_id = int(results[0].boxes.cls[0].item())
                class_name = results[0].names[class_id]
            except Exception as e:
                result = {"error": f"Model tahmin hatası: {e}"}
                return render_template("index.html", result=result)

            match = csv_data[csv_data["title"].str.lower().str.strip() == class_name.lower().strip()]
            if not match.empty:
                row = match.iloc[0]
                result = {
                    "artist": row["artist"],
                    "title": row["title"],
                    "jpg_url": row.get("jpg url", ""),
                    "description": row["description"]
                }

                
                artist_name = row["artist"].strip()
                similar = csv_data[
                    (csv_data["artist"].str.strip() == artist_name) &
                    (csv_data["title"] != row["title"])
                ]
                suggestions = similar.sample(n=min(3, len(similar))).to_dict(orient="records") if not similar.empty else []

            else:
                result = {"error": f"'{class_name}' adlı tablo veritabanında bulunamadı."}

    return render_template("index.html", result=result, suggestions=suggestions)


@app.route("/camera")
def camera_capture():
    result = None
    suggestions = []

    try:
        
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()

        if not ret:
            raise Exception("Kamera görüntüsü alınamadı.")

        
        tmp_filename = f"static/uploads/{uuid.uuid4().hex}.jpg"
        cv2.imwrite(tmp_filename, frame)

        
        results = model(tmp_filename)
        
        if results[0].boxes.cls.numel() == 0:
            result = {"error": "Model görselde tablo bulamadı."}
            return render_template("index.html", result=result)

        class_id = int(results[0].boxes.cls[0].item())
        class_name = results[0].names[class_id]

        
        match = csv_data[csv_data["title"].str.lower().str.strip() == class_name.lower().strip()]
        if not match.empty:
            row = match.iloc[0]
            result = {
                "artist": row["artist"],
                "title": row["title"],
                "jpg_url": row.get("jpg url", ""),
                "description": row["description"]
            }

            artist_name = row["artist"].strip()
            similar = csv_data[
                (csv_data["artist"].str.strip() == artist_name) &
                (csv_data["title"] != row["title"])
            ]
            suggestions = similar.sample(n=min(3, len(similar))).to_dict(orient="records") if not similar.empty else []

        else:
            result = {"error": f"'{class_name}' adlı tablo veritabanında bulunamadı."}

    except Exception as e:
        result = {"error": f"Kamera tanıma hatası: {e}"}

    return render_template("index.html", result=result, suggestions=suggestions)



@app.route('/video_feed')
def video_feed():
    def generate_video():
        cap = cv2.VideoCapture(0)
        while True:
            success, frame = cap.read()
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()

                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    return Response(generate_video(), mimetype='multipart/x-mixed-replace; boundary=frame')



@app.route("/artwork/<title>")
def artwork_detail(title):
    match = csv_data[csv_data["title"].str.lower().str.strip() == title.lower().strip()]
    if not match.empty:
        row = match.iloc[0]
        result = {
    "artist": row["artist"],
    "title": row["title"],
    "jpg_url": row.get("jpg url", ""),  
    "description": row["description"]
}


        
        artist_name = row["artist"].strip()
        similar = csv_data[
            (csv_data["artist"].str.strip() == artist_name) &
            (csv_data["title"] != row["title"])
        ]

       
        suggestions = similar.sample(n=min(3, len(similar))).to_dict(orient="records") if not similar.empty else []

        return render_template("index.html", result=result, suggestions=suggestions)
    else:
        return render_template("index.html", result={"error": "Bu başlığa ait tablo bulunamadı."})

if __name__ == "__main__":
    app.run(debug=True)