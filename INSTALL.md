# INSTALL.md

If you are reading this document, it means you absolutely want to run an instance of this bot yourself. Do note that this is not for the faint of heart, and as such, you must know what you're doing.

## Prerequisites

Before you begin, you must have Python 3.6 or above installed. Linux distros (such as Ubuntu, Arch Linux, Linux Mint, Zorin) already have this (it may require an update), but if you have macOS, you need to install it [here](https://www.python.org/downloads/).

Pip is required for this, and by default, it's already installed into Python for you. If not, go [here](https://pip.pypa.io/en/stable/installing/) to install it.

Now, with all of that being said, you need to install the `discord` package. Then you need to install these packages:

* lavalink
* asyncpg
* requests
* lxml

To install them, run `python3 -m pip install -U --user <package>`, replacing `<package>` with each of the packages listed.

Alternatively, you can also run `pip install -r requirements.txt --user` to install all of them at once.

If you are on Linux, you need to install `libffi-dev` (or `libffi-devel` for some distros) for installing the Discord rewrite, as one of the dependencies (PyNaCl) needs that library for voice support to work. You have to use your distro's package management tool for this.

## API Tokens

You absolutely **must** acquire these keys yourself. I am not getting them for you.

* Discord API Token (you can get them from the Developer's Portal on discordapp.com)
* News API Token

## Unobtainable API tokens

* DiscordBots.org API token

## Initializing database

This is entirely optional, but if you plan on having the bot use a database, you need to download PostgreSQL and
create a database called "axiro". The bot will setup the database for you.

## How to get this bot running

1. Place all API Tokens in where they should go in `config.json`. That file needs to be created.
2. Install the requirements listed above.
3. If you want the music module to work, follow the instructions in the section below called "Getting the Music module to work" before moving on to the next step.
4. Run `python core.py`. Substitute `python` with `python3` or `py` if `python` does not work.

## Getting the Music module to work

Note 1: As of this writing, Java 11 or newer is required for Lavalink to work. It can be downloaded [here](https://www.oracle.com/technetwork/java/javase/overview/index.html).

Note 2: If you're on macOS, you will need to download Java 8 from [Oracle](https://www.oracle.com/technetwork/java/javase/overview/index.html) (requires account) or [AdoptOpenJDK](https://adoptopenjdk.net/) (no account needed) instead, for reasons that will become clear in step 1.

1. If you are on Windows or Linux, download the latest build of Lavalink [here](https://ci.fredboat.com/viewLog.html?buildId=lastSuccessful&buildTypeId=Lavalink_Build&tab=artifacts&guest=1). Mac users will need to download [this build](https://github.com/Cog-Creators/Lavalink-Jars/releases/download/3.2.1_846/Lavalink.jar) due to [this issue](https://github.com/Frederikam/Lavalink/issues/180). Java 9 and above will not work for that specific build.
2. Create the document `application.yml` in the same directory as your Lavalink build. You can use [this example](https://github.com/Frederikam/Lavalink/blob/master/LavalinkServer/application.yml.example).
3. Open a Terminal (or PowerShell if on Windows) in that directory, and run `java -jar Lavalink.jar`.

## The config.json

```json
{
    "discordtoken": "discordapp.com API token",
    "newsapitoken": "newsapi token",
    "lavalinkpass": "Lavalink password",
    "dbpass": "Database password",
    "dbuser": "Database username",
    "dbl_token": "DiscordBots.org token",
    "prefix": "x!",
    "lavaport": "2333",
}
```
