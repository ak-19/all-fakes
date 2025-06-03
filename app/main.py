from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from uuid import uuid4
import os

app = FastAPI(title="Mini TikTok Clone")
templates = Jinja2Templates(directory="app/templates")

# Data storage
USERS = {}
VIDEOS = {}
VIDEO_DIR = "videos"
os.makedirs(VIDEO_DIR, exist_ok=True)

class UserCreate(BaseModel):
    username: str


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.get("/watch", response_class=HTMLResponse)
async def watch(request: Request):
    """Render the swipeable video feed page."""
    return templates.TemplateResponse(request, "watch.html")


@app.post("/users")
async def create_user(user: UserCreate):
    user_id = str(uuid4())
    USERS[user_id] = {"id": user_id, "username": user.username}
    return USERS[user_id]

@app.post("/videos")
async def upload_video(
    user_id: str = Form(...),
    description: str = Form(""),
    file: UploadFile = File(...),
):
    if user_id not in USERS:
        raise HTTPException(status_code=404, detail="User not found")
    video_id = str(uuid4())
    file_ext = os.path.splitext(file.filename)[1]
    file_path = os.path.join(VIDEO_DIR, f"{video_id}{file_ext}")
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    VIDEOS[video_id] = {
        "id": video_id,
        "user_id": user_id,
        "description": description,
        "filename": file_path,
    }
    return VIDEOS[video_id]

@app.get("/feed")
async def feed():
    return list(VIDEOS.values())

@app.get("/videos/{video_id}")
async def get_video(video_id: str):
    video = VIDEOS.get(video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return FileResponse(video["filename"], media_type="video/mp4")
