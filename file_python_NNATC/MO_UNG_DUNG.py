import os
import subprocess

def find_file(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
    return None
file_path = find_file('Zalo.exe', 'C:/')
if file_path is None:
    file_path = find_file('Zalo.exe', 'D:/')
    if file_path is None:
        pass
        print('Không có Zalo trên máy')
subprocess.Popen([file_path])
