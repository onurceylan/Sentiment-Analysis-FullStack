# Temel Python imajı
FROM python:3.10-slim

# Çalışma dizini
WORKDIR /app

# Sistem bağımlılıkları
#RUN apt-get update && apt-get install -y --no-install-recommends \
#    build-essential \
#    gcc \
#    python3-dev \
#    && apt-get clean \
#    && rm -rf /var/lib/apt/lists/*

# requirements.txt dosyasını ayrı kopyala (önbellek avantajı için)
COPY requirements.txt .

# Python bağımlılıklarını yükle
RUN pip install --no-cache-dir -r requirements.txt

# Geri kalan her şeyi kopyala (app.py, pkl dosyaları vs.)
COPY . .

# Flask uygulamasını çalıştır
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]


# Flask uygulaması çalışsın
#CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:$PORT", "app:app"]



