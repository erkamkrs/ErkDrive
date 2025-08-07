from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Body, status, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.security import OAuth2PasswordBearer
from minio import Minio
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
import os
import io
import datetime
from app.auth import hash_password, verify_password, create_access_token, decode_token

from time import sleep

load_dotenv()

app = FastAPI(title="Drive Clone API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB
mongo_client = MongoClient(os.getenv("MONGO_URI"))
db = mongo_client["drive"]
files_collection = db["files"]


# OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
users_collection = db["users"]

@app.post("/register")
def register(email: str = Body(...), password: str = Body(...)):
    if users_collection.find_one({"email": email}):
        raise HTTPException(status_code=400, detail="Email already exists")
    
    user = {
        "email": email,
        "password": hash_password(password)
    }
    users_collection.insert_one(user)
    return {"message": "User registered successfully"}

@app.post("/login")
def login(email: str = Body(...), password: str = Body(...)):
    user = users_collection.find_one({"email": email})
    if not user or not verify_password(password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": user["email"]})
    return {"access_token": token, "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload["sub"]

# MinIO
minio_client = Minio(
    endpoint=os.getenv("MINIO_ENDPOINT").replace("http://", ""),
    access_key=os.getenv("MINIO_ACCESS_KEY"),
    secret_key=os.getenv("MINIO_SECRET_KEY"),
    secure=False,
)

BUCKET = "uploads"
if not minio_client.bucket_exists(BUCKET):
    minio_client.make_bucket(BUCKET)

@app.post("/folders")
def create_folder(name: str):
    folder_id = str(ObjectId())
    files_collection.insert_one({
        "_id": folder_id,
        "filename": name,
        "is_folder": True,
        "upload_date": datetime.datetime.utcnow(),
        "folder": "root"  # or another folder id
    })
    return {"message": "Folder created", "id": folder_id}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...), folder: str = "root"):
    contents = await file.read()
    file_id = str(ObjectId())
    minio_client.put_object(
        bucket_name=BUCKET,
        object_name=file_id,
        data=io.BytesIO(contents),
        length=len(contents),
        content_type=file.content_type,
    )
    doc = {
        "_id": file_id,
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(contents),
        "upload_date": datetime.datetime.utcnow(),
        "folder": folder
    }
    files_collection.insert_one(doc)
    return {"message": "Uploaded successfully", "id": file_id}

@app.get("/files")
def list_files(folder: str = "root"):
    files = list(files_collection.find({"folder": folder}))
    for f in files:
        f["id"] = str(f["_id"])
        del f["_id"]
    return files


@app.get("/download/{file_id}")
def download_file(file_id: str):
    try:
        obj = minio_client.get_object(BUCKET, file_id)
        metadata = files_collection.find_one({"_id": file_id})
        if not metadata:
            raise HTTPException(status_code=404, detail="Metadata not found")
        return StreamingResponse(obj, media_type=metadata["content_type"],
                                 headers={"Content-Disposition": f"attachment; filename={metadata['filename']}"})
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.put("/files/{file_id}")
def rename_file(file_id: str, new_name: str):
    result = files_collection.update_one(
        {"_id": file_id}, {"$set": {"filename": new_name}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="File not found")
    return {"message": "Renamed successfully"}


@app.delete("/files/{file_id}")
def delete_file(file_id: str):
    try:
        minio_client.remove_object(BUCKET, file_id)
        files_collection.delete_one({"_id": file_id})
        return {"message": "Deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
