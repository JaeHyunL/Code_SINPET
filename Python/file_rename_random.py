import os
from uuid import uuid4

paths = ['D:\JaeHyun227',]

for path in paths:
    for file in os.listdir(path):
        if os.path.isdir(file):
            continue
        basename, ext = os.path.basename(file).split('.')
        basename = uuid4()
        rename = f"{basename}.{ext}"
        os.rename(os.path.join(path, file), f"{os.path.join(path, rename)}")
