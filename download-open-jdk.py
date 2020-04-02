import requests

from clint.textui import progress

url = 'https://github.com/AdoptOpenJDK/openjdk11-binaries/releases/download/jdk-11.0.6%2B10/OpenJDK11U-jdk_x64_linux_hotspot_11.0.6_10.tar.gz'

r = requests.get(url, stream=True)

with open("OpenJDK11U-jdk_x64_linux_hotspot_11.0.6_10.tar.gz'", "wb") as Py.gz:

    total_length = int(r.headers.get('content-length'))

    for ch in progress.bar(r.iter_content(chunk_size = 2391975), expected_size=(total_length/1024) + 1):

        if ch:

            Py.tar.gz.write(ch)