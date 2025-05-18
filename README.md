# 🧠 Face Recognition API (Deep Learning-Based)

This is an end-to-end face recognition system built with **Python**, **FastAPI**, **DeepFace**, **PostgreSQL**, and **Docker**. It allows users to:

* 🧍 Detect and register faces
* 🔎 Recognize faces from images
* 🗂️ Store face embeddings in a database
* 📡 Access RESTful API endpoints
* 🖼️ View original uploaded face images

---

## 🚀 Features

* **Face Detection**: Detect exactly one face using RetinaFace
* **Feature Extraction**: Extract embeddings with Facenet512
* **Face Matching**: Match against database with cosine similarity
* **REST API**: Register, recognize, list, and delete faces
* **PostgreSQL**: Stores embeddings and metadata
* **Static Images**: Stores original uploaded images
* **Dockerized**: Easily deployable with Docker

---

## 📦 Tech Stack

* **Backend**: FastAPI
* **Face Processing**: [DeepFace](https://github.com/serengil/deepface)
* **Model**: RetinaFace + Facenet512
* **Database**: PostgreSQL with SQLAlchemy ORM
* **Storage**: Local static folder (`/static`)
* **Containerization**: Docker, Docker Compose

---

## 🛠️ Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/mfakhrulam/face-recog-api.git
cd face-recog-api
```

### 2. Create `.env` file or rename `.env.example` to `.env`

```env
STATIC_DIR="static"
POSTGRES_USER="postgres"
POSTGRES_PASSWORD="password"
POSTGRES_DB="db_face_recog"
HOST="face_db"
POSTGRES_PORT="5432"
```

### 3. Run with Docker

```bash
docker-compose up --build
```

It will start:

* FastAPI at: `http://localhost:8000`
* Swagger Docs at: `http://localhost:8000/docs`
* Static images at: `http://localhost:8000/static/<filename>`

### ⚠️ Note on First-Time Run

The first time you use the **register** or **recognize** API endpoints, the process might take a while because pre-trained models (such as RetinaFace and Facenet512 from DeepFace) need to be downloaded.

This is a one-time download. Once the models are cached locally inside the container, subsequent runs will be much faster.

If you've already built the image once, you don't need to use the `--build` flag again. Just run:

```bash
docker-compose up
```

to start the application without re-downloading the models or rebuilding the image.

---

## 📡 API Endpoints

| Method | Endpoint              | Description                    |
| ------ | --------------------- | ------------------------------ |
| GET    | `/api/face`           | List all registered faces      |
| POST   | `/api/face/register`  | Register a new face            |
| POST   | `/api/face/recognize` | Recognize a face from an image |
| DELETE | `/api/face/{id}`      | Delete a face by ID            |

---

## 📤 Register a Face

**Request:**

```http
POST /api/face/register
Content-Type: multipart/form-data
Form-data:
  - name: string
  - file: image/jpeg
```

**Returns:**

```json
{
  "id": 1,
  "name": "Alice",
  "image_path": "/static/alice.jpg",
  "cropped_image_path": "/static/crop_alice.jpg"
}
```

---

## 📥 Recognize a Face

**Request:**

```http
POST /api/face/recognize
Content-Type: multipart/form-data
Form-data:
  - file: image/jpeg
```

**Returns:**

```json
{
  "matched": true,
  "id": 1,
  "name": "Alice",
  "image_path": "/static/alice.jpg",
  "cropped_image_path": "/static/crop_alice.jpg",
  "score": 0.978
}
```

Or if no match:

```json
{
  "matched": false,
  "detail": "No match found."
}
```

## 📥 Delete a Face

**Request:**

```http
DELETE /api/face/<int:id>
```

**Returns:**

```json
{
  "deleted": 3
}
```


---

## 📂 Folder Structure

```
face-recognition-api/
├── app/
│   ├── main.py              # FastAPI routes
│   ├── models.py            # SQLAlchemy models
│   ├── database.py          # DB connection
│   ├── face_utils.py        # Face detection & embedding
│   ├── crud.py              # CRUD process to DB
│   ├── requirements.txt     # Library requirements
│   └── static/              # Uploaded original images
├── Dockerfile
├── docker-compose.yml
├── init.sql
├── .env.example
└── README.md
```

---

## 🧪 Testing

You can test the endpoints directly from:

* Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
* Postman or curl

---

## ✅ Notes

* Only images with **exactly one face** are allowed. Multiple/no face will raise `400 Bad Request`.
* Embeddings are extracted with **Facenet512** model.
* Distance threshold can be adjusted (default `0.5`).

---

## 📄 License

MIT — feel free to use and modify.

