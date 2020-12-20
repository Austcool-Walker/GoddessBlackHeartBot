#!/bin/zsh
if [[ "$OSTYPE" == "linux-gnu" ]]; then
        Linux/Contents/Home/bin/java -jar -Xmx1G Lavalink.jar
elif [[ "$OSTYPE" == "darwin"* ]]; then
        macOS/Contents/Home/bin/java -jar -Xmx1G Lavalink.jar
elif [[ "$OSTYPE" == "cygwin" ]]; then
        # POSIX compatibility layer and Linux environment emulation for Windows
elif [[ "$OSTYPE" == "msys" ]]; then
        # Lightweight shell and GNU utilities compiled for Windows (part of MinGW)
elif [[ "$OSTYPE" == "win32" ]]; then
        # I'm not sure this can happen.
elif [[ "$OSTYPE" == "freebsd"* ]]; then
        # ...
else
        # Unknown.
        echo "Your OSTYPE could not be detected!"
fi
