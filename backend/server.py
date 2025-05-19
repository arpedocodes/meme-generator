from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
import uuid
import json
from logic.server.main import get_meme



app = FastAPI()

# Allow frontend access (adjust as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Make sure data folder exists
os.makedirs(os.path.join("logic","server","data"), exist_ok=True)

@app.get("/")
async def root():
    return {"message": "Welcome to the Meme Generator API!"}

@app.post("/meme")
async def receive_images(
    annotatedImage: UploadFile = File(...),
    originalImage: UploadFile = File(...),
    rectangleData: str = Form(...)
):
    # Parse rectangle JSON data
    try:
        rect_data = json.loads(rectangleData)
        # print(rect_data)
        with open(os.path.join("logic","server","data","rectangleData.json"), "w") as f:
            json.dump(rect_data, f)
    except json.JSONDecodeError:
        return JSONResponse(status_code=400, content={"error": "Invalid JSON for rectangleData"})

    # Generate unique ID
    submission_id = str(uuid.uuid4())

    # File paths
    annotated_path = f"logic/server/data/{submission_id}_annotated.png"
    original_path = f"logic/server/data/{submission_id}_original.png"

    # Save input images
    with open(annotated_path, "wb") as f:
        shutil.copyfileobj(annotatedImage.file, f)

    with open(original_path, "wb") as f:
        shutil.copyfileobj(originalImage.file, f)

    paths = get_meme(annotated_path, original_path)

    url = []
    for path in paths:
        # Move the output image to the output directory
        output_path = os.path.join("output", os.path.basename(path))
        url.append(output_path)


    # Respond with image paths
    return {
        "data": {
            "images": url,
        }
    }

@app.get("/output/{file_id}")
async def get_data(file_id: str):
    # Check if the submission ID exists
    if not os.path.exists(os.path.join("logic","server","output", file_id)):
        return JSONResponse(status_code=404, content={"error": "Submission ID not found"})

    # Get the paths of the images
    requested_image = os.path.join("logic","server","output", file_id)

    return FileResponse(
        path=requested_image,
        media_type="image/png",
        filename=os.path.basename(requested_image)
    )