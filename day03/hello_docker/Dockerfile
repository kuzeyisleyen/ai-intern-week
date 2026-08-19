#Python sürümü seçiyoruz
FROM python:3.9-slim
# Konteyner içindeki çalışma dizinimizi belirliyoruz
WORKDIR /app
#app.py dosyasını konteynerin içine kopyalıyoruz
COPY app.py .
# Konteyner ayağa kalktığında çalıştırılacak varsayılan komut
CMD ["python","app.py"]