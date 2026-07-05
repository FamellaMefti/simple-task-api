Aplikasi REST API sederhana (Python + Flask) untuk mengelola daftar task (to-do list).
Proyek ini dibuat untuk Tugas Praktikum Terintegrasi: Docker, Container Orchestration, dan CI/CD.

## Struktur Folder

```
simple-task-api/
├── app.py               # Definisi Flask app & routes
├── tests/
│   └── test_app.py      # Automated test (pytest)
├── pytest.ini
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .gitignore
└── .github/
    └── workflows/
        └── ci.yml        # Pipeline GitHub Actions
```

## Menjalankan Secara Lokal (tanpa Docker)

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
# Aplikasi berjalan di http://localhost:3000
```

## Menjalankan Test

```bash
pytest
```

## Menjalankan dengan Docker

```bash
docker build -t simple-task-api:v1 .
docker run -d --name simple-task-api -p 8080:3000 simple-task-api:v1
docker ps
```

Aplikasi dapat diakses di `http://localhost:8080`.

## Menjalankan dengan Docker Compose

```bash
docker compose up -d
docker compose ps
docker compose down
```

## Endpoint API

| Method | Endpoint      | Deskripsi                     |
|--------|---------------|--------------------------------|
| GET    | /health       | Health check                  |
| GET    | /             | Info aplikasi & daftar endpoint |
| GET    | /tasks        | Ambil semua task              |
| GET    | /tasks/:id    | Ambil satu task                |
| POST   | /tasks        | Buat task baru (`{ "title": "..." }`) |
| PUT    | /tasks/:id    | Update task (`title`/`done`)   |
| DELETE | /tasks/:id    | Hapus task                    |

Contoh cek kesehatan:

```bash
curl http://localhost:8080/health
# {"status":"healthy"}
```

## CI/CD

Setiap push/pull request ke branch `main` akan menjalankan pipeline GitHub Actions
(`.github/workflows/ci.yml`) yang melakukan:

1. Checkout source code
2. Install dependency (`pip install -r requirements.txt`)
3. Menjalankan automated test (`pytest`)
4. Build Docker image

