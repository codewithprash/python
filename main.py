from fastapi import FastAPI, HTTPException
import qrcode
import pyqrcode
import os
import pyqrcodeng as pyqrcode
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

QR_CODE_DIR = "https://universel-qr.onrender.com/"

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the QR Code Generator"}

@app.get("/png/{data}")
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
    file_path = f"{QR_CODE_DIR}{data}.png"
    img.save(f"{data}.png")
    return {"image_path": file_path}