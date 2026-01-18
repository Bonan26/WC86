#!/usr/bin/env python3
"""Generate image with reference image for style"""
import requests, base64, sys

API_KEY = "AIzaSyDO6tt-Ft4zdkm8GZws8lp_bNw2l-zYM40"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp-image-generation:generateContent?key={API_KEY}"

def gen_with_ref(ref_image_path: str, prompt: str, output: str):
    # Read reference image
    with open(ref_image_path, "rb") as f:
        ref_data = base64.b64encode(f.read()).decode()

    # Determine mime type
    mime = "image/png" if ref_image_path.endswith(".png") else "image/jpeg"

    r = requests.post(API_URL, json={
        "contents": [{
            "parts": [
                {"inlineData": {"mimeType": mime, "data": ref_data}},
                {"text": f"Using this wolf character image as style reference, generate a new image: {prompt}. Keep the exact same cartoon illustration style, line work, and color palette. Solid black background for easy removal."}
            ]
        }],
        "generationConfig": {"responseModalities": ["IMAGE", "TEXT"]}
    }, timeout=120)

    for c in r.json().get("candidates", []):
        for p in c.get("content", {}).get("parts", []):
            if "inlineData" in p:
                with open(output, "wb") as f:
                    f.write(base64.b64decode(p["inlineData"]["data"]))
                print(f"Saved: {output}")
                return
    print(f"No image found. Response: {r.text[:500]}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3 gen_image_with_ref.py <ref_image> <output.png> <prompt>")
    else:
        gen_with_ref(sys.argv[1], " ".join(sys.argv[3:]), sys.argv[2])
