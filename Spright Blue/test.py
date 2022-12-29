import youtube_dl

yt_dl_opts = {
    'format': 'bestaudio',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ytdl = youtube_dl.YoutubeDL(yt_dl_opts)

urlYT = "https://www.youtube.com/watch?v=VgUDOJ_9wmM&ab_channel=M4rkim"
data_music = ytdl.extract_info(url=urlYT, download=False)
print(f"{data_music['title']} | {data_music['channel']}")