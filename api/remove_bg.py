from rembg import remove
from PIL import Image
import io

def handler(request):
    try:
        # Handle CORS preflight
        if request.method == "OPTIONS":
            return {
                "status": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type",
                },
                "body": "OK"
            }

        # Only POST requests
        if request.method != "POST":
            return {"status": 405, "body": "Method Not Allowed"}

        # Get uploaded image
        image_file = request.files.get("image")
        if not image_file:
            return {"status": 400, "body": "No image uploaded"}

        # Open image
        input_bytes = image_file.read()
        input_img = Image.open(io.BytesIO(input_bytes)).convert("RGBA")

        # Remove background
        output_img = remove(input_img)

        # Convert to bytes
        output_buffer = io.BytesIO()
        output_img.save(output_buffer, format="PNG")
        output_bytes = output_buffer.getvalue()

        return {
            "status": 200,
            "headers": {
                "Content-Type": "image/png",
                "Access-Control-Allow-Origin": "*",  # CORS
            },
            "body": output_bytes
        }

    except Exception as e:
        return {"status": 500, "body": f"Error: {str(e)}"}
