import os
import yt_dlp
from django.http import JsonResponse, FileResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import uuid
import tempfile
import requests
from urllib.parse import urlparse


# Create your views here.

def home(request):
    return render(request, "core/index.html")



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


# @csrf_exempt
# def download_video(request):
#     if request.method == "POST":
#         url = request.POST.get("url")
#         if not url:
#             return HttpResponseBadRequest("No URL provided")
#
#         url = resolve_tiktok_url(url)
#
#         try:
#             temp_dir = tempfile.mkdtemp()
#             filename = str(uuid.uuid4())
#
#             ydl_opts = {
#                 # This format string is robust. It finds the best video and audio streams,
#                 # even if they are served in separate files and with different codecs.
#                 "format": "bestvideo+bestaudio/best",
#                 "outtmpl": os.path.join(temp_dir, f"{filename}.%(ext)s"),
#                 # This postprocessor will merge the streams and re-encode to the
#                 # specified codecs.
#                 "postprocessors": [{
#                     "key": "FFmpegVideoRemuxer",
#                     "preferedformat": "mp4",
#                 }],
#                 "postprocessor_args": {
#                     "ffmpeg": [
#                         "-c:v", "libx264",
#                         "-c:a", "aac",
#                         "-strict", "experimental",
#                     ]
#                 }
#             }
#
#             with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#                 info = ydl.extract_info(url, download=True)
#                 file_path = ydl.prepare_filename(info)
#
#             return FileResponse(
#                 open(file_path, "rb"),
#                 as_attachment=True,
#                 filename=os.path.basename(file_path)
#             )
#
#         except Exception as e:
#             # For debugging, let's print the actual error to the console
#             print(f"yt-dlp error: {e}")
#             return JsonResponse({"error": str(e)}, status=400)
#
#     return HttpResponseBadRequest("Invalid request")

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
                # This is the key part: re-encode the video with ffmpeg
                "postprocessors": [{
                    "key": "FFmpegVideoConvertor",
                    "preferedformat": "mp4",
                }],
                # Download the best video and best audio separately, then merge
                "format": "bestvideo+bestaudio/best",
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)

                # yt-dlp returns the file path of the final, converted video
                file_path = ydl.prepare_filename(info)

            # Return the file as a downloadable response
            return FileResponse(
                open(file_path, "rb"),
                as_attachment=True,
                filename=os.path.basename(file_path)
            )

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return HttpResponseBadRequest("Invalid request")