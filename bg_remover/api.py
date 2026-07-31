from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response
from bg_remover.core import remove_background_bytes

app = FastAPI(title="Background Remover API")

@app.post("/api/remove-bg")
async def remove_bg(file: UploadFile = File(...), model: str = "u2net"):
    """
    Upload an image file and receive the image with its background removed.
    """
    input_data = await file.read()
    try:
        output_data = remove_background_bytes(input_data, model_name=model)
        return Response(content=output_data, media_type="image/png")
    except Exception as e:
        return Response(content=f"Error processing image: {str(e)}", status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("bg_remover.api:app", host="0.0.0.0", port=8000, reload=True)
