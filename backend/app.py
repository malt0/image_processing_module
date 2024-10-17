from fastapi import FastAPI, UploadFile, File, HTTPException
from celery.result import AsyncResult
from tasks import process_image_task
from fastapi.responses import JSONResponse
import os

app = FastAPI()

# Ensure directories exist
UPLOAD_DIR = 'uploads/'
PROCESSED_DIR = 'processed/'

# Create directories if they don't exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

@app.post("/process-image/")
async def process_image(file: UploadFile = File(...), operation: str = 'grayscale'):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPEG and PNG are allowed.")
    
    # Save uploaded image
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as f:
        f.write(await file.read())
    
    # Send task to Celery
    task = process_image_task.delay(file_location, operation)
    
    return {"task_id": task.id, "message": "Image processing started"}


# Check task status
@app.get("/task-status/{task_id}")
async def get_task_status(task_id: str):
    task_result = AsyncResult(task_id)
    if task_result.state == 'PENDING':
        return {"task_id": task_id, "status": "Pending"}
    elif task_result.state != 'FAILURE':
        return {"task_id": task_id, "status": task_result.state, "result": task_result.result}
    else:
        return {"task_id": task_id, "status": "Failure", "message": str(task_result.info)}

# Retrieve processed image (optional)
@app.get("/task-result/{task_id}")
async def get_task_result(task_id: str):
    task_result = AsyncResult(task_id)
    
    if task_result.state == 'SUCCESS':
        processed_image_path = task_result.result
        if os.path.exists(processed_image_path):
            return JSONResponse(content={"task_id": task_id, "processed_image": processed_image_path})
        else:
            raise HTTPException(status_code=404, detail="Processed image not found.")
    else:
        return {"task_id": task_id, "status": task_result.state}

