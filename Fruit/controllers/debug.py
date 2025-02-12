import os
from django.http import JsonResponse
from django.conf import settings

def check_model_file(request):
    model_path = os.path.join(settings.BASE_DIR, "Fruit", "models", "shape_classifier.h5")

    if os.path.exists(model_path):
        return JsonResponse({"status": "OK", "message": "Le fichier existe", "path": model_path})
    else:
        return JsonResponse({"status": "ERROR", "message": "Le fichier n'existe pas", "path": model_path})
