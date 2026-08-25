# 1. Temel image
FROM python:3.10-slim

# 2. Çalışma dizini
WORKDIR /app

# 3. Bağımlılıkları önce kopyala ve kur.
COPY requirements.txt .

RUN python -m pip install --no-cache-dir -r requirements.txt

# 4. Proje kodlarını kopyala.
COPY . .

# 5. Varsayılan komut.
CMD ["python", "-m", "day04.tool_call_demo", "İstanbul'dan Ankara'ya 2 desi kargo ne kadar tutar?"]