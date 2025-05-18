from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from pgvector.sqlalchemy import Vector
from settings import DATABASE_URL
from database import Base

class Face(Base):
  __tablename__ = "faces"
  id = Column(Integer, primary_key=True)
  name = Column(String, nullable=False)
  embedding = Column(Vector(512))  # 512-dim vector for Facenet512
  image_path = Column(String, nullable=False)
  cropped_image_path = Column(String, nullable=False)

# # Create DB session
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Create table
# Base.metadata.create_all(bind=engine)
