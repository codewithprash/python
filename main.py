from fastapi import FastAPI, HTTPException
import qrcode
from io import BytesIO

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/generate_qr/")
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

    img_io = BytesIO()
    img.save(img_io, format="PNG")
    img_io.seek(0)

    return StreamingResponse(content=img_io, media_type="image/png")
