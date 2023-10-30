import os
import subprocess


for rr in os.listdir('kakaoDownload'):


    command = "ffmpeg -i '{}' -ab 160k -ac 2 -ar 44100 -vn '{}'".format(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'kakaoDownload', rr),
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'kakaoConvert', os.path.basename(rr))
    )

    subprocess.call(command, shell=True, text=True)
