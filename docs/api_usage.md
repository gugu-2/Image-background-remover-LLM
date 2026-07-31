# API Usage Guide

The Background Remover includes a built-in FastAPI web server. This allows you to host the tool as a microservice and integrate background removal into your own web apps, mobile apps, or automated workflows.

## Starting the API Server

To start the server locally for development, activate your virtual environment and run:

```bash
python -m bg_remover.api
```

You should see output indicating that Uvicorn is running on `http://0.0.0.0:8000`.

## Interactive API Documentation (Swagger)

FastAPI automatically generates an interactive documentation page. Once the server is running, open your web browser and go to:

[http://localhost:8000/docs](http://localhost:8000/docs)

From here, you can click on the `POST /api/remove-bg` endpoint, click **"Try it out"**, upload an image file from your computer, and see the background removed live in your browser!

## API Endpoint Details

- **URL:** `/api/remove-bg`
- **Method:** `POST`
- **Content-Type:** `multipart/form-data`
- **Body:** Form data containing a single file field named `file`.
- **Response:** The raw binary data of the processed `.png` image (Content-Type: `image/png`).

## Code Examples

### 1. cURL

```bash
curl -X POST "http://localhost:8000/api/remove-bg" \
  -H "accept: image/png" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/image.jpg" \
  --output result_nobg.png
```

### 2. Python (using `requests`)

```python
import requests

url = "http://localhost:8000/api/remove-bg"
file_path = "image.jpg"

with open(file_path, "rb") as f:
    files = {"file": f}
    response = requests.post(url, files=files)

if response.status_code == 200:
    with open("result.png", "wb") as f_out:
        f_out.write(response.content)
    print("Background removed successfully!")
else:
    print("Error:", response.text)
```

### 3. JavaScript (using `fetch`)

```javascript
const fileInput = document.querySelector('input[type="file"]');
const file = fileInput.files[0];

const formData = new FormData();
formData.append('file', file);

fetch('http://localhost:8000/api/remove-bg', {
  method: 'POST',
  body: formData
})
.then(response => response.blob())
.then(blob => {
  const imageUrl = URL.createObjectURL(blob);
  const imgElement = document.createElement('img');
  imgElement.src = imageUrl;
  document.body.appendChild(imgElement);
})
.catch(error => console.error('Error:', error));
```
