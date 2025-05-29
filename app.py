from flask import Flask, render_template, request
import pickle
import nltk
from nltk.corpus import stopwords

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
        return render_template("index.html", error="Lütfen bir yorum girin!", review=review)

    # Metni vektöre çevir ve tahmin yap
    try:
        vec = vectorizer.transform([review])
        pred = model.predict(vec)[0]
        label = "Positive" if pred == 1 else "Negative"
        return render_template("index.html", review=review, prediction_text=label)
    except Exception as e:
        return render_template("index.html", error=f"Tahmin yapılırken hata oluştu: {str(e)}", review=review)


if __name__ == "__main__":
    app.run(debug=True)