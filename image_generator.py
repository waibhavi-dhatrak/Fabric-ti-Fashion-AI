
import os
import requests
import base64
from io import BytesIO
from dotenv import load_dotenv

load_dotenv(".env", override=True)

CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")
CLOUDFLARE_ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID")

MODEL = "@cf/black-forest-labs/flux-1-schnell"


def generate_fashion_image(
    fabric_analysis,
    fashion_design,
    occasion,
    audience
):
    if not CLOUDFLARE_API_TOKEN or not CLOUDFLARE_ACCOUNT_ID:
        raise ValueError("Cloudflare credentials are missing from .env")

    url = (
        f"https://api.cloudflare.com/client/v4/accounts/"
        f"{CLOUDFLARE_ACCOUNT_ID}/ai/run/{MODEL}"
    )

    prompt = f"""
    Create a photorealistic full-body fashion editorial image.

    Fabric: {fabric_analysis.fabric_type}
    Main colour: {fabric_analysis.primary_color}
    Other colours: {", ".join(fabric_analysis.secondary_colors[:3])}
    Pattern: {fabric_analysis.pattern}
    Texture: {fabric_analysis.texture}

    Design concept: {fashion_design.design_concepts[0] if fashion_design.design_concepts else "Elegant contemporary outfit"}
    Garment: {fashion_design.garment_recommendations[0] if fashion_design.garment_recommendations else "Designer outfit"}
    Styling: {fashion_design.styling_suggestions[0] if fashion_design.styling_suggestions else "Minimal elegant styling"}

    Occasion: {occasion}
    Audience: {audience}

    Preserve the fabric's colours, pattern and texture.
    Show realistic fabric folds and detailed garment construction.
    Full-body professional fashion photography.
    Clean studio background. No text or watermark.
    """

    if len(prompt) > 2048:
        prompt = prompt[:2048]

    headers = {
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": prompt,
        "steps": 4
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=180
    )

    if response.status_code != 200:
        raise Exception(
            f"Cloudflare API error {response.status_code}: "
            f"{response.text}"
        )

    data = response.json()
    image_base64 = data.get("result", {}).get("image")

    if not image_base64:
        raise Exception("Cloudflare did not return an image.")

    image_bytes = base64.b64decode(image_base64)

    if not image_bytes:
        raise Exception("Generated image is empty.")

    return BytesIO(image_bytes)
