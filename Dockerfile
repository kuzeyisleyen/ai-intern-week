# 1. Temel imaj
FROM python:3.9-slim

# 2. Çalışma dizini
WORKDIR /app

# 3. Önce bağımlılık listesini kopyala ve kur (Cache optimizasyonu için)
# DÜZELTME 1: Artık ana dizindeki doğru requirements.txt dosyasını okuyoruz
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

# 4. Projedeki tüm kodları kopyala (.dockerignore sayesinde output/ kopyalanmayacak)
COPY . .

# 5. Konteyner hiçbir komut verilmeden çalıştırılırsa varsayılan olarak ne yapsın?
# DÜZELTME 2: Eski day03 yerine, varsayılan olarak yeni ajanımızı test etsin
CMD ["python", "-m", "day04.tool_call_demo", "İstanbul'dan Ankara'ya 2 desi kargo ne kadar tutar?"]