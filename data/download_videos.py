import yt_dlp

fil = open('youtube_ids.txt', 'r')
lines = fil.readlines()
URLS = ['https://youtu.be/' + line.strip() for line in lines]

ydl_opts = {
    #'format': 'mp4',
    'outtmpl': 'downloaded_videos/%(id)s.%(ext)s'
}

ydl = yt_dlp.YoutubeDL(ydl_opts)

for url in URLS:
    try:
        error_code = ydl.download([url])
    except Exception as e:
        print(f'Failed to download video: {url}')

