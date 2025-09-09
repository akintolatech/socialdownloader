import os
import yt_dlp
from django.http import JsonResponse, FileResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import tempfile
import uuid
import tempfile
import requests
from urllib.parse import urlparse


# Create your views here.

def home(request):
    return render(request, "core/index.html")


@csrf_exempt
# def download_video(request):
#     if request.method == "POST":
#         url = request.POST.get("url")
#         if not url:
#             return HttpResponseBadRequest("No URL provided")
#
#         try:
#             # Create a temporary folder to save downloads
#             temp_dir = tempfile.mkdtemp()
#             filename = str(uuid.uuid4())  # random unique name
#
#             ydl_opts = {
#                 "outtmpl": os.path.join(temp_dir, f"{filename}.%(ext)s"),
#             }
#
#             with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#                 info = ydl.extract_info(url, download=True)
#                 file_path = ydl.prepare_filename(info)
#
#             # Return file as a downloadable response
#             response = FileResponse(open(file_path, "rb"), as_attachment=True, filename=os.path.basename(file_path))
#             return response
#
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=400)
#
#     return HttpResponseBadRequest("Invalid request")



def resolve_tiktok_url(url: str) -> str:
    """
        Helper function to resolve urls that may have problems
        Resolve TikTok Lite shortened links (vm.tiktok.com) into full TikTok URLs.
    """
    try:
        parsed = urlparse(url)
        # Handle Tiktok Urls by expanding into full urls
        if "vm.tiktok.com" in parsed.netloc:
            response = requests.head(url, allow_redirects=True, timeout=10)
            return response.url
    except Exception:
        pass
    return url  # return original if not TikTok or resolve fails

@csrf_exempt
def download_video(request):
    if request.method == "POST":
        url = request.POST.get("url")
        if not url:
            return HttpResponseBadRequest("No URL provided")

        # Handle TikTok Lite special case
        url = resolve_tiktok_url(url)

        try:
            # Temporary folder for downloads
            temp_dir = tempfile.mkdtemp()
            filename = str(uuid.uuid4())

            ydl_opts = {
                "outtmpl": os.path.join(temp_dir, f"{filename}.%(ext)s"),
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info)

            return FileResponse(
                open(file_path, "rb"),
                as_attachment=True,
                filename=os.path.basename(file_path)
            )

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return HttpResponseBadRequest("Invalid request")