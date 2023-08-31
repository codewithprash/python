import base64
import io
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import qrcode
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


origins = [
    "https://upiqrcode.pages.dev",
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


@app.get("/qr/{data}")
async def generate_qr_code(data: str):
    if not data:
        raise HTTPException(status_code=400, detail="Data parameter is required")

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    code = f"upi://pay?cu=INR&pa={data}"
    qr.add_data(code)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image as a PNG file
    file_path = f"{data}.png"
    img.save(file_path)

    

    return FileResponse(file_path)

@app.get("/qr_png/{code}")
async def generate_qr_code(code: str):
    if not code:
        raise HTTPException(status_code=400, detail="Code parameter is required")

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    data = f"upi://pay?cu=INR&pa={code}"
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Convert the image to base64
    img_io = io.BytesIO()
    img.save(img_io, format="PNG")
    img_io.seek(0)
    img_base64 = base64.b64encode(img_io.read()).decode()

    return {"image": img_base64}
