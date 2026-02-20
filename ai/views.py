from django.shortcuts import render
from django.conf import settings
# Create your views here.
import os
import requests
import base64
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

HF_KEY = settings.HF_KEY

@csrf_exempt
def generate_image(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    data = json.loads(request.body)
    prompt = data.get("prompt")

    API_URL = os.getenv("HF_MODEL_URL")

    headers = {
        "Authorization": f"Bearer {HF_KEY}",
        "Content-Type": "application/json"
    }


    payload = {
    "inputs": prompt,
    "parameters": {
        "negative_prompt": "blurry, low quality, distorted",
        "num_inference_steps": 30,
        "guidance_scale": 7.5
    }
}


    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        print("HF ERROR:", response.text)
        return JsonResponse({"error": response.text}, status=500)

    # Convert image bytes to base64
    image_base64 = base64.b64encode(response.content).decode("utf-8")

    return JsonResponse({"image": image_base64})
