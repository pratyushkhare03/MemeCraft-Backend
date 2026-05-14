from django.shortcuts import render
from django.conf import settings
import os
import requests
import base64
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import google.generativeai as genai

# HF_KEY = settings.HF_KEY

genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

# @csrf_exempt
# def generate_image(request):
#     if request.method != "POST":
#         return JsonResponse({"error": "Invalid request"}, status=400)

#     data = json.loads(request.body)
#     prompt = data.get("prompt")

#     API_URL = os.getenv("HF_MODEL_URL")

#     headers = {
#         "Authorization": f"Bearer {HF_KEY}",
#         "Content-Type": "application/json"
#     }


#     payload = {
#     "inputs": prompt,
#     "parameters": {
#         "negative_prompt": "blurry, low quality, distorted",
#         "num_inference_steps": 30,
#         "guidance_scale": 7.5
#     }
# }


#     response = requests.post(API_URL, headers=headers, json=payload)

#     if response.status_code != 200:
#         print("HF ERROR:", response.text)
#         return JsonResponse({"error": response.text}, status=500)

#     # Convert image bytes to base64
#     image_base64 = base64.b64encode(response.content).decode("utf-8")

#     return JsonResponse({"image": image_base64})


NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")


@csrf_exempt
def generate_image(request):

    if request.method != "POST":
        return JsonResponse(
            {"error": "Invalid request"},
            status=400
        )

    try:
        data = json.loads(request.body)
        prompt = data.get("prompt")

        if not prompt:
            return JsonResponse(
                {"error": "Prompt is required"},
                status=400
            )

        # NVIDIA Qwen Image endpoint
        API_URL = "https://integrate.api.nvidia.com/v1/images/generations"

        headers = {
            "Authorization": f"Bearer {NVIDIA_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "qwen/qwen-image",
            "prompt": prompt,
            "negative_prompt": "blurry, low quality, distorted",
            "size": "1024x1024",
            "quality": "high",
            "n": 1
        }

        response = requests.post(
            API_URL,
            headers=headers,
            json=payload
        )

        if response.status_code != 200:
            print("NVIDIA ERROR:", response.text)

            return JsonResponse(
                {"error": response.text},
                status=response.status_code
            )

        result = response.json()

        # Base64 image returned by API
        image_base64 = result["data"][0]["b64_json"]

        return JsonResponse({
            "image": image_base64
        })

    except Exception as e:
        return JsonResponse({
            "error": str(e)
        }, status=500)

@csrf_exempt
def generate_captions(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            prompt = body.get("prompt", "").strip()

            if not prompt:
                return JsonResponse({"error": "No prompt provided"}, status=400)

            print("USER PROMPT:", prompt)  # Debug check

            response = model.generate_content(prompt)

            return JsonResponse({
                "text": response.text
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)