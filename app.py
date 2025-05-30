from flask import Flask, render_template, request
import pickle
import os
import gdown

def download_models():
    model_url = "https://drive.google.com/file/d/125EI9dUj_wxtLuTBJGTXcGfAyVWk7op_/view?usp=drive_link"
    vec_url = "https://drive.google.com/file/d/1Q8_PKM-cVY-5M8Fs1gHrDVyMXVI14M_y/view?usp=sharing"

    try:
        if not os.path.exists("model.pkl"):
            print("Downloading model...")
            gdown.download(model_url, "model.pkl", quiet=False)

        if not os.path.exists("vectorizer.pkl"):
            print("Downloading vectorizer...")
            gdown.download(vec_url, "vectorizer.pkl", quiet=False)
    except FileExistsError:
        print("Model veya vectorizer dosyası indirilemedi!")
        exit(1)

# Flask uygulamasını başlat
app = Flask(__name__)
app.secret_key = "your-secret-key"  # Güvenlik için secret_key ekledik

# Model ve vectorizer'ı yükle
try:
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("vectorizer.pkl", "rb") as f:
        vectorizer = pickle.load(f)
except FileNotFoundError:
    print("Model veya vectorizer dosyası bulunamadı!")
    exit(1)


# Ana sayfa
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


# Tahmin endpoint'i
@app.route("/predict", methods=["POST"])
def predict():
    # Kullanıcının yorumunu al
    review = request.form.get("review", "").strip()

    # Boş yorum kontrolü
    if not review:
        return render_template("index.html", error="please make a comment!", review=review)

    # Metni vektöre çevir ve tahmin yap
    try:
        vec = vectorizer.transform([review])
        pred = model.predict(vec)[0]
        label = "Positive" if pred == 1 else "Negative"
        return render_template("index.html", review=review, prediction_text=label)
    except Exception as e:
        return render_template("index.html", error=f"an error occured when prediction was made: {str(e)}", review=review)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render PORT değişkeni sağlar
    app.run(host='0.0.0.0', port=port)
