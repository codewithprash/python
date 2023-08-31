from fastapi import FastAPI, HTTPException
import qrcode
import pyqrcode
import os

app = FastAPI()

# Configure CORS


# Define a directory to save the generated QR code images
QR_CODE_DIR = "qr_codes"

@app.get("/")
async def read_root():
    return {"message": "Welcome to the QR Code Generator"}

@app.get("/qr_code/{data}")
async def generate_qr_code(data: str):
    qr = pyqrcode.create(data)
    return {"qr_code": qr.png_as_base64_str(scale=5)}

@app.get("/generateqr")
async def generate_qr_code(data: str):
    if not data:
        raise HTTPException(status_code=400, detail="Data parameter is required")

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image as a PNG file
    file_path = os.path.join(QR_CODE_DIR, f"{data}.png")
    img.save(file_path)

    return {"image_path": file_path}



