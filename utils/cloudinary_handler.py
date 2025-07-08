import cloudinary
import cloudinary.uploader
import cloudinary.utils

from dotenv import load_dotenv
import os

load_dotenv() 
# Setup Cloudinary

cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("CLOUD_API_KEY"),
    api_secret=os.getenv("CLOUD_API_SECRET"),
    secure=True
)
def upload_to_cloudinary(local_path, folder, public_id):
    return cloudinary.uploader.upload(
        local_path,
        folder=folder,
        public_id=public_id
    )

def background_removal(public_id):
    url, _ = cloudinary.utils.cloudinary_url(
        f"background_removed/{public_id}",
        transformation=[
            {
                "effect": "background_removal",
                "crop": "fill",
                "format": "png"
            }
        ],
        format="png",
        secure=True
    )
    return url

def content_aware_resize(public_id):
    url, _ = cloudinary.utils.cloudinary_url(
        f"content_aware/{public_id}",
        transformation=[
            {
                "width": 1080,
                "height": 1440,
                "crop": "pad",
                "gravity": "west",
                "background": "gen_fill:prompt_a simple studio floor"
            }
        ],
        format="png",
        secure=True
    )
    return url

def add_shadow(public_id):
    url, _ = cloudinary.utils.cloudinary_url(
        f"bg_shadow_test/{public_id}",
        transformation=[
            {
                "effect": "dropshadow",
                "azimuth": 90,
                "elevation": 10,
                "spread": 0
            }
        ],
        format="png",
        secure=True
    )
    return url
