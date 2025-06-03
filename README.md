# Mini TikTok Clone

This project is a simple demonstration of how you might implement a TikTok-like API using [FastAPI](https://fastapi.tiangolo.com/).

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Endpoints

- `POST /users` – Create a new user. Body: `{"username": "example"}`
- `POST /videos` – Upload a video. Form field `file` (video) and JSON body containing `user_id` and optional `description`.
- `GET /feed` – Retrieve the list of uploaded videos.
- `GET /videos/{video_id}` – Download a specific video file.

Uploaded files are stored in the `videos/` directory.
