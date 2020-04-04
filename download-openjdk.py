import requests
from clint.textui import progress
from sys import platform as _platform

if _platform == "linux" or _platform == "linux2":
    # linux
    url = 'https://github.com/AdoptOpenJDK/openjdk11-binaries/releases/download/jdk-11.0.6%2B10/OpenJDK11U-jdk_x64_linux_hotspot_11.0.6_10.tar.gz'
    #target_path = 'OpenJDK11U-jdk_x64_linux_hotspot_11.0.6_10.tar.gz'

    r = requests.get(url, stream=True)
    path = 'OpenJDK11U-jdk_x64_linux_hotspot_11.0.6_10.tar.gz'
    with open(path, 'wb') as f:
        total_length = int(r.headers.get('content-length'))
        for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
            if chunk:
                f.write(chunk)
                f.flush()
elif _platform == "darwin":
    # MAC OS X
    url = 'https://github.com/AdoptOpenJDK/openjdk11-binaries/releases/download/jdk-11.0.6%2B10/OpenJDK11U-jdk_x64_mac_hotspot_11.0.6_10.tar.gz'
    #target_path = 'OpenJDK11U-jdk_x64_mac_hotspot_11.0.6_10.tar.gz'

    r = requests.get(url, stream=True)
    path = 'OpenJDK11U-jdk_x64_mac_hotspot_11.0.6_10.tar.gz'
    with open(path, 'wb') as f:
        total_length = int(r.headers.get('content-length'))
        for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
            if chunk:
                f.write(chunk)
                f.flush()
elif _platform == "win32":
    # Windows
    url = 'https://github.com/AdoptOpenJDK/openjdk11-binaries/releases/download/jdk-11.0.6%2B10/OpenJDK11U-jdk_x86-32_windows_hotspot_11.0.6_10.zip'
    #target_path = 'OpenJDK11U-jdk_x86-32_windows_hotspot_11.0.6_10.zip'

    r = requests.get(url, stream=True)
    path = 'OpenJDK11U-jdk_x64_linux_hotspot_11.0.6_10.tar.gz'
    with open(path, 'wb') as f:
        total_length = int(r.headers.get('content-length'))
        for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
            if chunk:
                f.write(chunk)
                f.flush()
elif _platform == "win64":
    # Windows 64-bit
    url = 'https://github.com/AdoptOpenJDK/openjdk11-binaries/releases/download/jdk-11.0.6%2B10/OpenJDK11U-jdk_x64_windows_hotspot_11.0.6_10.zip'
    #target_path = 'OpenJDK11U-jdk_x64_windows_hotspot_11.0.6_10.zip'

    r = requests.get(url, stream=True)
    path = 'OpenJDK11U-jdk_x64_windows_hotspot_11.0.6_10.zip'
    with open(path, 'wb') as f:
        total_length = int(r.headers.get('content-length'))
        for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
            if chunk:
                f.write(chunk)
                f.flush()