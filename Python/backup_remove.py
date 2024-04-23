import os
import sys

from datetime import datetime, timedelta

target_path = sys.argv[1]
# print(sys.argv)
if not os.listdir(target_path):
    sys.exit(0)

def remove_file_choice(file_list: list) -> list:
    remove_file_list = []
    for file in file_list:
        try:
            unix_time = file.split('_')[0]
        except Exception:
            continue
        # 대충 문자 형식만 파악하기 위해 하드코딩
        if not 1600000000 < int(unix_time) < 2000000000:
            continue
        ft = datetime.utcfromtimestamp(int(unix_time))
        nt = datetime.now()
        if nt - ft > timedelta(days=30):
            remove_file_list.append(file)
    return remove_file_list


for root, _, files in os.walk(target_path):
    target = remove_file_choice(files)
    for t in target:
        remove_file = os.path.join(root, t)
        try:
            os.remove(remove_file)
        except PermissionError:
            # 분기처리를 할까...?
            continue
        except FileExistsError:
            # 말까?
            continue
        except FileNotFoundError:
             # 할까?
            continue
