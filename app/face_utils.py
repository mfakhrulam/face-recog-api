from deepface import DeepFace
import cv2
import os
import uuid
from settings import STATIC_DIR
import numpy as np

# supported backends
backends = [
    'opencv', 'ssd', 'dlib', 'mtcnn', 'fastmtcnn',
    'retinaface', 'mediapipe', 'yolov8', 'yolov11s',
    'yolov11n', 'yolov11m', 'yunet', 'centerface',
]

# supported models
models = [
    "VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace",
    "DeepID", "ArcFace", "Dlib", "SFace", "GhostFaceNet",
    "Buffalo_L",
]

detector = backends[5] # retinaface
align = True
model = models[2] # Facenet512

def normalize_image(img):
  if img.dtype == np.float32 or img.dtype == np.float64:
    img = np.clip(img, 0.0, 1.0)
    img = (img * 255).astype(np.uint8)
  return img
  
def detect_and_crop_face(image_path: str) -> str:
  try:
    faces = DeepFace.extract_faces(
      img_path=image_path,
      detector_backend=detector,
      align=True,
      enforce_detection=True
    )
  except ValueError as ev:
    message = str(ev)
    if message.startswith("Face could not be detected"):
      raise ValueError("No face detected.")
  
  if len(faces) > 1:
    raise ValueError("Multiple faces detected.")
  
  cropped_face = faces[0]["face"]
  cropped_face = normalize_image(cropped_face)
  cropped_filename = f"crop_{uuid.uuid4().hex}.jpg"
  cropped_path = os.path.join(STATIC_DIR, cropped_filename)
  cv2.imwrite(cropped_path, cv2.cvtColor(cropped_face, cv2.COLOR_RGB2BGR))
    
  return cropped_path

def extract_features(face_path: str) -> list:
  embedding_obj = DeepFace.represent(
    img_path=face_path,
    model_name=model,
    detector_backend="skip", # no need to use detector again
    enforce_detection=False # already do detection on the face
  )[0]

  return embedding_obj["embedding"]

def cosine_similarity(a: list[float], b: list[float]) -> float:
  a = np.array(a)
  b = np.array(b)
  return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
