import base64
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
import json
import os
from django.shortcuts import render, redirect
from django.http import JsonResponse


def home(request):
    return render(request, 'aggregator/home.html')


@csrf_exempt
def save_cropped_image(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            image_data = data.get('image_data', '')

            # Decode base64 image data
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            file_name = f"cropped_image.{ext}"

            # Save the image
            file_path = os.path.join("media", "cropped", file_name)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "wb") as f:
                f.write(base64.b64decode(imgstr))

            return JsonResponse({'status': 'success', 'file_path': file_path})
        except Exception as e:
            return JsonResponse({'status': 'failed', 'error': str(e)})
    return JsonResponse({'status': 'failed', 'error': 'Invalid request method.'})
