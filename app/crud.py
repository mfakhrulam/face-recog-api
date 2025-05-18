from models import Face
from database import SessionLocal
from sqlalchemy import func
import os

def list_faces():
  db = SessionLocal()
  faces = db.query(Face).all()
  return [
      {"id": f.id, "name": f.name, "image_path": f.image_path, "cropped_image_path": f.cropped_image_path}
      for f in faces
  ]
  
def list_faces_with_embeddings():
  db = SessionLocal()
  faces = db.query(Face).all()
  return faces

def register_face(name, embedding, image_path, cropped_image_path):
  db = SessionLocal()
  new_face = Face(name=name, 
                  embedding=embedding, 
                  image_path=image_path, 
                  cropped_image_path=cropped_image_path)
  db.add(new_face)
  db.commit()
  db.refresh(new_face)
  return new_face

def delete_face_by_id(face_id):
  db = SessionLocal()
  face = db.query(Face).get(face_id)
  if not face:
    return False
  if os.path.exists(face.image_path):
    os.remove(face.image_path)
  if os.path.exists(face.cropped_image_path):
    os.remove(face.cropped_image_path)
  db.delete(face)
  db.commit()
  return True

def recognize_face(embedding, threshold=0.5):
  db = SessionLocal()
  results = (
    db.query(Face, func.cosine_distance(Face.embedding, embedding).label("similarity"))
    .order_by("similarity")
    .limit(1)
  ).first()

  if results and results.similarity < (1 - threshold):
    return results.Face
  return None
