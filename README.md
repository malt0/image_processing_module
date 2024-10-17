# Image Processing with FastAPI, Celery, and Redis

This project demonstrates an image processing pipeline using **FastAPI** as the backend API, **Celery** for asynchronous task processing, and **Redis** as the message broker. It allows users to upload images, process them asynchronously (grayscale or resize), and retrieve the results.

## Features
- Upload images via an API endpoint.
- Asynchronous task processing with Celery.
- Retrieve task status and processed images.
- Supports image operations like grayscale and resizing.

## Project Structure

```
image_processing_demo/
│
├── backend/
│   ├── app.py          # FastAPI app with API endpoints
│   ├── tasks.py        # Celery tasks for image processing
│   ├── celery_worker.py # Celery worker starter
│   ├── celeryconfig.py  # Celery configuration
│
├── Dockerfile (Optional)
├── requirements.txt    # Python dependencies
└── README.md           # Documentation (this file)
```

## Requirements

- Python 3.8+
- Redis (as the message broker for Celery)
- FastAPI
- Celery
- Pillow (for image processing)
- Uvicorn (for serving FastAPI)
  
You can install dependencies from the `requirements.txt` file.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/image-processing-demo.git
   cd image-processing-demo
   ```

2. **Set up a virtual environment (optional but recommended):**
   ```bash
   python3 -m venv env
   source env/bin/activate  # On Windows use: env\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start Redis:**
   If you don't have Redis installed, you can use Docker to run it:
   ```bash
   docker run -p 6379:6379 -d redis
   ```

5. **Start FastAPI:**
   Start the FastAPI server using `uvicorn`:
   ```bash
   uvicorn app:app --reload
   ```

6. **Start the Celery worker:**
   In a separate terminal, run the Celery worker:
   ```bash
   celery -A tasks worker --loglevel=info
   ```

## API Endpoints

### 1. Upload Image and Start Processing
This endpoint allows you to upload an image and specify the image processing task.

**Endpoint:**
```
POST /process-image/
```

**Form Data:**
- `file` (File): The image file (JPEG or PNG).
- `operation` (String): The image processing operation. Supported operations:
  - `grayscale`: Converts the image to grayscale.
  - `resize`: Resizes the image to 100x100 pixels.

**Example Request in Postman:**
- Method: **POST**
- URL: `http://127.0.0.1:8000/process-image/`
- Body: `form-data`
  - `file`: Upload your image (JPEG or PNG).
  - `operation`: `grayscale` or `resize`.

**Example Response:**
```json
{
  "task_id": "f8a5d96e-ff1f-4d9d-bc67-b1c6b9dbec1f",
  "message": "Image processing started"
}
```

### 2. Check Task Status
This endpoint returns the current status of the image processing task (e.g., pending, started, or completed).

**Endpoint:**
```
GET /task-status/{task_id}
```

**Parameters:**
- `task_id` (String): The ID of the task to check the status.

**Example Request in Postman:**
- Method: **GET**
- URL: `http://127.0.0.1:8000/task-status/{task_id}`

**Example Response (Pending Task):**
```json
{
  "task_id": "f8a5d96e-ff1f-4d9d-bc67-b1c6b9dbec1f",
  "status": "PENDING"
}
```

**Example Response (Completed Task):**
```json
{
  "task_id": "f8a5d96e-ff1f-4d9d-bc67-b1c6b9dbec1f",
  "status": "SUCCESS",
  "result": "processed/your-image-name.jpg"
}
```

### 3. Retrieve Processed Image Result (Optional)
Once the task is completed, you can retrieve the processed image.

**Endpoint:**
```
GET /task-result/{task_id}
```

**Parameters:**
- `task_id` (String): The ID of the task to get the result.

**Example Request in Postman:**
- Method: **GET**
- URL: `http://127.0.0.1:8000/task-result/{task_id}`

**Example Response:**
```json
{
  "task_id": "f8a5d96e-ff1f-4d9d-bc67-b1c6b9dbec1f",
  "processed_image": "processed/your-image-name.jpg"
}
```

---

## How to Use Postman to Test the API

1. **Upload Image**: 
   - Use the `POST /process-image/` endpoint in Postman to upload an image and start processing.
   - You'll receive a `task_id` in the response.

2. **Check Task Status**: 
   - Use the `GET /task-status/{task_id}` endpoint with the `task_id` you received in step 1 to check if the image processing is complete.

3. **Retrieve Processed Image**: 
   - (Optional) Once the task is complete, you can use the `GET /task-result/{task_id}` endpoint to retrieve the processed image file path.

---

## Monitoring Celery Tasks

You can monitor Celery tasks by running a **Flower** instance:
```bash
pip install flower
celery -A tasks flower
```
Then navigate to `http://localhost:5555` to see Celery task progress.

---

## Notes

- Ensure that you have proper permissions to write files to the `uploads/` and `processed/` directories.
- The processed images will be saved in the `processed/` directory by default.

## License
This project is open-source and available under the [MIT License](LICENSE).
