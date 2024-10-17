from celery import Celery
from PIL import Image
import os

# Initialize Celery
app = Celery('tasks', broker='redis://localhost:6379/0')

# Image processing task
@app.task(bind=True)
def process_image_task(self, image_path: str, operation: str = 'grayscale'):
    try:
        # Open the image
        img = Image.open(image_path)

        # Apply selected operation
        if operation == 'grayscale':
            img = img.convert("L")
        elif operation == 'resize':
            img = img.resize((100, 100))  # Resize to a small thumbnail as an example
        else:
            raise ValueError("Unsupported operation")

        # Save processed image
        processed_image_path = f"processed/{os.path.basename(image_path)}"
        img.save(processed_image_path)

        return processed_image_path

    except Exception as e:
        self.update_state(state='FAILURE', meta={'error': str(e)})
        raise e
