import yt_dlp
import sys
import os

if len(sys.argv) < 4:
    print("Eksik parametre! Lütfen video URL'sini, kaydedilecek dosya yolunu ve formatı belirtin.")
    sys.exit(1)

def download_video(video_url, base_path, format_type):
    ffmpeg_path = 'C:/ffmpeg-7.1.1-full_build/bin/ffmpeg.exe'
    ydl_opts = {}

    if format_type == 'mp3':
        ydl_opts = {
            'username': 'mira.elmira1111@gmail.com',
            'password':'5PTi0Cgk',
            'format': 'bestaudio',
            'outtmpl': base_path + '.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'ffmpeg_location': ffmpeg_path,
            'verbose': True,
        }
    elif format_type == 'mp4':
 
        ydl_opts = {
        'username': 'mira.elmira1111@gmail.com',
        'password':'5PTi0Cgk',
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
        'outtmpl': base_path + '.mp4',
        'ffmpeg_location': ffmpeg_path,
        'merge_output_format': 'mp4',
        'verbose': True
    }

    else:
        print("Desteklenmeyen format! 'mp3' veya 'mp4' belirtin.")
        sys.exit(1)

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
            return base_path
    except Exception as e:
        print(f"Download failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    video_url = sys.argv[1]
    base_path = sys.argv[2]
    format_type = sys.argv[3].lower()
    download_video(video_url, base_path, format_type)
