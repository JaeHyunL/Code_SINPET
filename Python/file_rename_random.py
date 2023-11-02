import os
from uuid import uuid4

paths = [
    'D:\JaeHyun226', 'D:\JaeHyun241', 'D:\JaeHyun242',
    'D:\JaeHyun244', 'D:\JaeHyun246', 'D:\JaeHyun247',
    'D:\JaeHyun248', 'D:\JaeHyun228', 'D:\JaeHyun249',
    'D:\JaeHyun250', 'D:\JaeHyun'
]

for path in paths:
    for file in os.listdir(path):
        if os.path.isdir(file):
            continue
        basename, ext = os.path.basename(file).split('.')
        basename = uuid4()
        rename = f"{basename}.{ext}"
        os.rename(os.path.join(path, file), f"{os.path.join(path, rename)}")
