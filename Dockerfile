# 1. Temel imaj
FROM python:3.9-slim

# 2. Çalışma dizini
WORKDIR /app

# 3. Önce bağımlılık listesini kopyala ve kur (Cache optimizasyonu için)
COPY day03/requirements-docker.txt ./requirements-docker.txt
RUN python -m pip install --no-cache-dir -r requirements-docker.txt

# 4. Projedeki tüm kodları kopyala (.dockerignore sayesinde output/ kopyalanmayacak)
COPY . .

# 5. Konteyner hiçbir komut verilmeden çalıştırılırsa varsayılan olarak ne yapsın?
CMD ["python", "day03/text_cli.py", "Docker icindeki varsayilan CMD calisti!"]