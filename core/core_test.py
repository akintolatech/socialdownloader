import yt_dlp

def download_video(url):
    ydl_opts = {
        'outtmpl': '%(title)s.%(ext)s',  # Save as video title
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

video_url = input("Enter video URL (Instagram, TikTok, Facebook): ")
download_video(video_url)