import os
import yt_dlp
from django.http import JsonResponse, FileResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import tempfile
import uuid


# Create your views here.

def home(request):
    return render(request, "core/index.html")


@csrf_exempt
def download_video(request):
    if request.method == "POST":
        url = request.POST.get("url")
        if not url:
            return HttpResponseBadRequest("No URL provided")

        try:
            # Create a temporary folder to save downloads
            temp_dir = tempfile.mkdtemp()
            filename = str(uuid.uuid4())  # random unique name

            ydl_opts = {
                "outtmpl": os.path.join(temp_dir, f"{filename}.%(ext)s"),
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info)

            # Return file as a downloadable response
            response = FileResponse(open(file_path, "rb"), as_attachment=True, filename=os.path.basename(file_path))
            return response

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return HttpResponseBadRequest("Invalid request")
