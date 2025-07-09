from fastapi import FastAPI, UploadFile, File, HTTPException
import os, uuid, traceback

from utils.cloudinary_handler import (
    upload_to_cloudinary, background_removal,
    content_aware_resize, add_shadow
)
from utils.download_utils import download_from_url
from utils.s3_handler import upload_to_s3

app = FastAPI()

TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)

@app.post("/background-removal/")
async def remove_background(file: UploadFile = File(...)):
    try:
        temp_path = f"{TEMP_DIR}/{uuid.uuid4().hex}_{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(await file.read())

        public_id = uuid.uuid4().hex
        upload_to_cloudinary(temp_path, "background_removed", public_id)

        result_url = background_removal(public_id)
        output_path = f"{TEMP_DIR}/output_{file.filename}"
        download_success = download_from_url(result_url, output_path)

        if not download_success:
            raise Exception("Failed to download processed image from Cloudinary.")

        s3_input_url = upload_to_s3(temp_path, "input")
        s3_output_url = upload_to_s3(output_path, "output")

        if not s3_input_url or not s3_output_url:
            raise Exception("S3 upload failed. Check AWS credentials or permissions.")

        return {
            "status": "success",
            "message": "Image processed and uploaded successfully.",
            "data": {
                "input_file_name": file.filename,
                "cloudinary_url": result_url,
                "s3_output_url": s3_output_url
            }
        }

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "message": "Image processing failed.",
            "details": str(e)
        })

@app.post("/content-aware/")
async def content_aware(file: UploadFile = File(...)):
    try:
        temp_path = f"{TEMP_DIR}/{uuid.uuid4().hex}_{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(await file.read())

        public_id = uuid.uuid4().hex
        upload_to_cloudinary(temp_path, "content_aware", public_id)

        result_url = content_aware_resize(public_id)
        output_path = f"{TEMP_DIR}/output_{file.filename}"
        download_success = download_from_url(result_url, output_path)

        if not download_success:
            raise Exception("Failed to download processed image from Cloudinary.")

        s3_input_url = upload_to_s3(temp_path, "input")
        s3_output_url = upload_to_s3(output_path, "output")

        if not s3_input_url or not s3_output_url:
            raise Exception("S3 upload failed. Check AWS credentials or permissions.")

        return {
            "status": "success",
            "message": "Image processed and uploaded successfully.",
            "data": {
                "input_file_name": file.filename,
                "cloudinary_url": result_url,
                "s3_output_url": s3_output_url
            }
        }

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "message": "Image processing failed.",
            "details": str(e)
        })


@app.post("/add-shadow/")
async def shadow_add(file: UploadFile = File(...)):
    try:
        temp_path = f"{TEMP_DIR}/{uuid.uuid4().hex}_{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(await file.read())

        public_id = uuid.uuid4().hex
        upload_to_cloudinary(temp_path, "bg_shadow_test", public_id)

        result_url = add_shadow(public_id)
        output_path = f"{TEMP_DIR}/output_{file.filename}"
        download_success = download_from_url(result_url, output_path)

        if not download_success:
            raise Exception("Failed to download processed image from Cloudinary.")

        s3_input_url = upload_to_s3(temp_path, "input")
        s3_output_url = upload_to_s3(output_path, "output")

        if not s3_input_url or not s3_output_url:
            raise Exception("S3 upload failed. Check AWS credentials or permissions.")

        return {
            "status": "success",
            "message": "Image processed and uploaded successfully.",
            "data": {
                "input_file_name": file.filename,
                "cloudinary_url": result_url,
                "s3_output_url": s3_output_url
            }
        }

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "message": "Image processing failed.",
            "details": str(e)
        })
