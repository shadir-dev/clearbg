import io
import os
import cgi
from http.server import BaseHTTPRequestHandler, HTTPServer
from rembg import remove
from PIL import Image

HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", 5000))

class BGRemover(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        if self.path != "/remove-bg":
            self.send_error(404, "Endpoint not found")
            return

        # Parse multipart/form-data
        content_type = self.headers.get("Content-Type")
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={"REQUEST_METHOD": "POST", "CONTENT_TYPE": content_type}
        )

        if "image" not in form:
            self.send_error(400, "No image uploaded with the name 'image'")
            return

        file_item = form["image"]
        image_bytes = file_item.file.read()

        try:
            # Open input image
            input_img = Image.open(io.BytesIO(image_bytes)).convert("RGBA")

            # Remove background
            output_img = remove(input_img)

            # Convert to bytes
            output_buffer = io.BytesIO()
            output_img.save(output_buffer, format="PNG")
            output_data = output_buffer.getvalue()

            # Send back the PNG
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Type", "image/png")
            self.send_header("Content-Length", str(len(output_data)))
            self.end_headers()
            self.wfile.write(output_data)

        except Exception as e:
            self.send_error(500, f"Error: {str(e)}")


    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Background Remover Server Running!")
        else:
            self.send_error(404, "Not Found")


# Run server
if __name__ == "__main__":
    print(f"Server running at http://{HOST}:{PORT}")
    HTTPServer((HOST, PORT), BGRemover).serve_forever()
