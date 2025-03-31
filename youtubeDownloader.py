import yt_dlp
import sys

# Parametrelerin doğru olduğundan emin olalım
if len(sys.argv) < 3:
    print("Eksik parametre! Lütfen video URL'sini ve kaydedilecek dosya yolunu belirtin.")
    print(f"Geçerli parametreler: {len(sys.argv)}")
    sys.exit(1)

def download_video(video_url, download_path):
    ydl_opts = {
        'format': 'bv+ba/b',  # Best video ve best audio'yu indir ve birleştir
        'outtmpl': download_path,  # Video kaydetme yolu
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
    video_url = sys.argv[1]  # Komut satırından gelen video URL'si
    download_path = sys.argv[2]  # Komut satırından gelen video kaydetme yolu
    download_video(video_url, download_path)
