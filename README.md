# 女神ブラックハート Note this is a modified fork or The Weirdness Mix (TWM) discord bot. This fork is modified to fit The Overcomplicated Weirdness (TOW) Discord server.

~~Axiro is a discord bot, designed to be weird and fun at the same time, as proven from this [Reddit thread](https://www.reddit.com/r/softwaregore/comments/ayfcbe/and_you_thought_student_debt_was_bad_try_discord/).~~

You can join the official server [here](https://discord.gg/veVDS47), or invite the bot with this [link](https://discordapp.com/api/oauth2/authorize?client_id=693568262813909072&permissions=8&scope=bot).

## Features:

* Basic encryption, decryption, and hash.
* Typical anime stuff.
* An economy run on chickens.
* Music capabilities
* Access the news.
* Do what admins need to do (kick, ban, etc.)

## Installation:

Please refer to the INSTALL.md file for instructions on how to run an instance of this bot.

## TODO:

* ~~Build the mute command.~~
* Add this bot to discordbots.org
* Get to 200 guilds.
* Gain access to weeb.sh
* ~~Use aiohttp for Konachan~~
* ~~Build music module.~~
* Add more cool bot functions/features.
* Complete the Encryption module.
lb

run
-------------
Either you start the script directly via `python3 main.py` or create a systemd unit, you can find an example under`GoddessBlackHeartBot.service`:

```
[Unit]
Description=GoddessBlackHeart Discord Bot
After=multi-user.target
[Service]
WorkingDirectory=/home/noire/Documents/GoddessBlackHeartBot
Environment="PYTHONHASHSEED=0"
User=noire
Group=noire
ExecStart=/usr/bin/python3 /home/noire/Documents/GoddessBlackHeartBot/GoddessBlackHeartBot.py
Type=idle
Restart=on-failure
RestartSec=15
TimeoutStartSec=15

[Install]
WantedBy=multi-user.target
```

Copy to `/ etc / systemd / system / GoddessBlackHeartBot.service` and adapt. Don't forget to start the unit via `sudo systemctl start GoddessBlackHeartBot.service` or autostart via` sudo systemctl enable GoddessBlackHeartBot.service`.
