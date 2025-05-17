from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from crud import register_face, list_faces, delete_face_by_id, recognize_face
from face_utils import detect_and_crop_face, extract_features
import cv2
import os
import uuid
import numpy as np
from fastapi.staticfiles import StaticFiles


STATIC_DIR = "static"
os.makedirs(STATIC_DIR, exist_ok=True)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/api/face")
def get_faces():
  return list_faces()

@app.post("/api/face/register")
async def register(name: str = Form(...), file: UploadFile = File(...)):
  contents = await file.read()
  
  filename = f"{name}_{uuid.uuid4().hex}.jpg"
  original_path = os.path.join(STATIC_DIR, filename)
  with open(original_path, "wb") as f:
    f.write(contents)
  
  try: 
    cropped_path = detect_and_crop_face(original_path)
    embedding = extract_features(cropped_path)
    
    face = register_face(name, embedding, f"/static/{filename}", f"/static/{cropped_path}")
    
    return {
      "id": face.id,
      "name": face.name,
      "image_path": face.image_path,
      "cropped_image_path": face.cropped_image_path
    }
    
  except ValueError as ve:
    if os.path.exists(original_path):
      os.remove(original_path)
    raise HTTPException(status_code=400, detail=str(ve))

  except Exception as e:
    if os.path.exists(original_path):
      os.remove(original_path)
    raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/api/face/recognize")
async def recognize(file: UploadFile = File(...)):
  contents = await file.read()
  filename = f"{uuid.uuid4().hex}.jpg"
  temp_path = os.path.join(STATIC_DIR, filename)
  with open(temp_path, "wb") as f:
    f.write(contents)
    
  try:
    cropped_path = detect_and_crop_face(temp_path)
    embedding = extract_features(cropped_path)
    match = recognize_face(embedding)
    os.remove(cropped_path)
    os.remove(temp_path)
    if match:
      return {
        "id": match.id,
        "name": match.name,
        "image_path": match.image_path,
      }
    else:
      return JSONResponse(
        content={"detail": "No match found."}, 
        status_code=404
      )
    
  
  except ValueError as ve:
    if os.path.exists(temp_path):
      os.remove(temp_path)
    raise HTTPException(status_code=400, detail=str(ve))

  except Exception as e:
    if os.path.exists(temp_path):
      os.remove(temp_path)
    raise HTTPException(status_code=500, detail="Internal server error")

@app.delete("/api/face/{face_id}")
def delete_face(face_id: int):
  success = delete_face_by_id(face_id)
  if not success:
    raise HTTPException(status_code=404, detail="Face not found.")
  return {"deleted": face_id}
