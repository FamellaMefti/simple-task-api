# Base image
FROM python:3.12-slim

# Working directory di dalam container
WORKDIR /usr/src/app

# Salin file dependency dahulu supaya cache layer Docker efisien
COPY requirements.txt ./

# Install dependency
RUN pip install --no-cache-dir -r requirements.txt

# Salin source code aplikasi
COPY app.py ./
COPY templates ./templates
COPY static ./static

# Port yang digunakan aplikasi
EXPOSE 3000

# Perintah untuk menjalankan aplikasi (gunicorn untuk production-ready server)
CMD ["gunicorn", "--bind", "0.0.0.0:3000", "app:create_app()"]
