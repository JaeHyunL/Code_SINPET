import os
from pytube import YouTube
import subprocess


# YouTube.
with open('list.txt', 'r') as f:
    read_txts = f.readlines()
    read_txts = [read_txts.strip() for read_txts in read_txts]

for music_uri in read_txts:
    yt = YouTube(music_uri)
    # print(yt)
    rr = yt.streams.filter(progressive=True, file_extension='mp4')\
        .order_by('resolution')\
        .desc()\
        .first()\
        .download('./musics')

    command = "ffmpeg -i {} -ab 160k -ac 2 -ar 44100 -vn {}".format(
        rr, os.path.join('./conver_wav', os.path.basename(rr))
    )

    subprocess.call(command, shell=True)
    os.path.dirname()
