from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import os
import shutil
import uuid
import json

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
os.makedirs("data", exist_ok=True)

@app.post("/")
async def receive_images(
    annotatedImage: UploadFile = File(...),
    originalImage: UploadFile = File(...),
    rectangleData: str = Form(...)
):
    # Parse rectangle JSON data
    try:
        rect_data = json.loads(rectangleData)
        with open("data/rectangleData.json", "w") as f:
            json.dump(rect_data, f)
    except json.JSONDecodeError:
        return JSONResponse(status_code=400, content={"error": "Invalid JSON for rectangleData"})

    # Generate unique ID
    submission_id = str(uuid.uuid4())

    # File paths
    annotated_path = f"data/{submission_id}_annotated.png"
    original_path = f"data/{submission_id}_original.png"
    processed1_path = f"data/{submission_id}_processed1.png"
    processed2_path = f"data/{submission_id}_processed2.png"

    # Save input images
    with open(annotated_path, "wb") as f:
        shutil.copyfileobj(annotatedImage.file, f)

    with open(original_path, "wb") as f:
        shutil.copyfileobj(originalImage.file, f)

    # Open and do dummy processing (copy images)
    img1 = Image.open(annotated_path)
    img2 = Image.open(original_path)

    img1.save(processed1_path)
    img2.save(processed2_path)

    # Respond with image paths
    return {
        "data": {
            "images": [
                annotated_path,
                original_path,
                processed1_path,
                processed2_path
            ]
        }
    }

@app.get("/data/{file_id}")
async def get_data(file_id: str):
    # Check if the submission ID exists
    if not os.path.exists(f"data/{file_id}"):
        return JSONResponse(status_code=404, content={"error": "Submission ID not found"})

    # Get the paths of the images
    requested_image = f"data/{file_id}"

    return FileResponse(
        path=requested_image,
        media_type="image/png",
        filename=os.path.basename(requested_image)
    )