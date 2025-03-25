import yt_dlp
import sys

def download_video(video_url):
    ydl_opts = {
        'format': 'bv+ba/b',  # Best video ve best audio'yu indir ve birleştir
        'outtmpl': 'Videos/downloaded_video.%(ext)s',
        'merge_output_format': 'mp4',  # Birleştirilen dosyanın formatı
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',  # Videoyu MP4 formatına çevir
        }],
        'postprocessor_args': [
            '-c:v', 'copy',  # Videoyu olduğu gibi kopyala
            '-c:a', 'aac', '-b:a', '192k'  # Sesi AAC formatına çevir
        ],
        'ffmpeg_location': 'C:/ffmpeg-7.1.1-full_build/bin/ffmpeg.exe',  # FFmpeg yolu
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

if __name__ == "__main__":
    video_url = sys.argv[1]  # Express'ten gelen URL
    download_video(video_url)
# https://www.youtube.com/watch?v=cWU9NM5uC6s&t=3s