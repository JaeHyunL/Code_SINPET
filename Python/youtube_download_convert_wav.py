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
    # 유투브 다운로드 오류시 해결방법 https://github.com/pytube/pytube/issues/84#issuecomment-1751541977
    # 일부 지원하지 않는 동영상에 대해서.
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


