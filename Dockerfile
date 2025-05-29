# Temel Python imajı
FROM python:3.10-slim

# Çalışma dizini
WORKDIR /app

# Gerekli dosyaları kopyala
COPY . /app

# Gerekli paketleri kur
RUN pip install --no-cache-dir -r requirements.txt

# Flask uygulaması çalışsın
CMD exec gunicorn app:app --bind 0.0.0.0:$PORT --workers 4

