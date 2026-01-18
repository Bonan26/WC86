#!/usr/bin/env python3
"""Generate one image with Gemini"""
import requests, base64, sys

API_KEY = "AIzaSyDO6tt-Ft4zdkm8GZws8lp_bNw2l-zYM40"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp-image-generation:generateContent?key={API_KEY}"

def gen(prompt: str, output: str):
    r = requests.post(API_URL, json={
        "contents": [{"parts": [{"text": f"Generate an image: {prompt}"}]}],
        "generationConfig": {"responseModalities": ["IMAGE", "TEXT"]}
    }, timeout=60)

    for c in r.json().get("candidates", []):
        for p in c.get("content", {}).get("parts", []):
            if "inlineData" in p:
                with open(output, "wb") as f:
                    f.write(base64.b64decode(p["inlineData"]["data"]))
                print(f"Saved: {output}")
                return
    print("No image found")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 gen_image.py <output.png> <prompt>")
    else:
        gen(" ".join(sys.argv[2:]), sys.argv[1])
