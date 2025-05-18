from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from crud import list_faces_with_embeddings, register_face, list_faces, delete_face_by_id, recognize_face
from face_utils import cosine_similarity, detect_and_crop_face, extract_features
import os
import uuid
import numpy as np
from fastapi.staticfiles import StaticFiles
from settings import STATIC_DIR
import models
from database import engine
import traceback

os.makedirs(STATIC_DIR, exist_ok=True)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
models.Base.metadata.create_all(bind=engine)

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
    
    face = register_face(name, embedding, f"/static/{filename}", f"/{cropped_path}")
    
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
    traceback.print_exc()

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
    
    known_faces = list_faces_with_embeddings()
    if not known_faces:
      raise HTTPException(status_code=404, detail="No registered faces in database.")

    os.remove(cropped_path)
    os.remove(temp_path)
    
    similarities = [
      (face, cosine_similarity(embedding, face.embedding)) for face in known_faces
    ]
    
    most_similar_face, score = max(similarities, key=lambda x: x[1])
    THRESHOLD = 0.5
    if score >= THRESHOLD:
      return {
        "matched": True,
        "id": most_similar_face.id,
        "name": most_similar_face.name,
        "image_path": most_similar_face.image_path,
        "cropped_image_path": most_similar_face.cropped_image_path,
        "score": score
      }
    else:
      return {"matched": False, "detail": "No match found."}

    # match = recognize_face(embedding)
    # os.remove(cropped_path)
    # os.remove(temp_path)
    # if match:
    #   return {
    #     "id": match.id,
    #     "name": match.name,
    #     "image_path": match.image_path,
    #     "cropped_image_path": match.cropped_image_path
    #   }
    # else:
    #   return JSONResponse(
    #     content={"detail": "No match found."}, 
    #     status_code=404
    #   )
    
  
  except ValueError as ve:
    if os.path.exists(temp_path):
      os.remove(temp_path)
    raise HTTPException(status_code=400, detail=str(ve))
  
  except HTTPException:
    raise
  
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
