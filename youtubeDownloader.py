import yt_dlp
import sys

# Parametrelerin doğru olduğundan emin olalım
if len(sys.argv) < 4:
    print("Eksik parametre! Lütfen video URL'sini, kaydedilecek dosya yolunu ve formatı belirtin.")
    sys.exit(1)

def download_video(video_url, download_path, format_type):
    # download_path burada uzantı eklenmeden geliyor. outtmpl içine ".%(ext)s" ekliyoruz.
    ydl_opts = {
        'format': 'bv+ba/b',  # Best video ve best audio'yu indir ve birleştir
        'outtmpl': download_path + ".%(ext)s",  # Dosya adı: base + FFmpeg tarafından belirlenecek uzantı
        'merge_output_format': 'mp4',  # Birleştirilen dosyanın formatı (video için)
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': format_type,  # İstenilen formatta dönüştür
        }],
        'ffmpeg_location': 'C:/ffmpeg-7.1.1-full_build/bin/ffmpeg.exe',  # FFmpeg yolu
    }

    if format_type == 'mp3':
        ydl_opts['postprocessor_args'] = [
            '-vn',              # Video kısmını atla
            '-acodec', 'libmp3lame',  # MP3 formatına dönüştür
            '-ab', '192k',      # Ses bit hızı
            '-ar', '44100',     # Ses örnekleme hızı
            '-ac', '2',         # Stereo ses kanalı
        ]
    else:
        ydl_opts['postprocessor_args'] = [
            '-c:v', 'copy',     # Videoyu olduğu gibi kopyala
            '-c:a', 'aac', '-b:a', '192k'  # Sesi AAC formatına çevir
        ]

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
    except Exception as e:
        print(f"İndirme sırasında hata oluştu: {e}")
        sys.exit(1)

if __name__ == "__main__":
    video_url = sys.argv[1]  # Komut satırından gelen video URL'si
    download_path = sys.argv[2]  # Komut satırından gelen dosya yolu (uzantı eklenmemiş)
    format_type = sys.argv[3]  # Komut satırından gelen format (mp4/mp3)
    download_video(video_url, download_path, format_type)
