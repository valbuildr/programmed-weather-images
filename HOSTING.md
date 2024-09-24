# Hosting

## Prerequisites
- [Python 3.12.6](https://www.python.org/downloads/release/python-3126/)
- A basic understanding of Python
- A Discord bot and the bot's token
- An API key from [weatherapi.com](https://weatherapi.com/)

## Obtaining a Discord bot token

> Note that "app" and "bot" are used interchangeably here.

1. Go to [discord.com/developers/applications](https://discord.com/developers/applications)
2. Log in to Discord.
3. Click "New Application" in the upper right.
4. Title your app and accept Discord's [Developer Terms of Service](https://support-dev.discord.com/hc/articles/8562894815383-Discord-Developer-Terms-of-Service) and [Developer Policy](https://support-dev.discord.com/hc/articles/8563934450327-Discord-Developer-Policy).
5. When the app is created, click the "Bot" tab in the left menu.
6. Click "Reset Token". You may be required to use a security key or type in your 2FA code.
7. Click "Copy" and save this in a safe place, we'll use it later!

## Obtaining a weatherapi.com token

1. Go to [weatherapi.com/signup.aspx](https://www.weatherapi.com/signup.aspx) and sign up for an account.
2. When signed up, go to "API Response Fields" in the menu in the left. (it's under "Dashboard")
3. Your API key will be shown in that page. Save this in a safe place, we'll use it later!

## Setting up the bot

1. Download the code from the [releases tab](https://github.com/valbuildr/programmed-weather-images/releases). *Get the "Source code (zip)" file.*
2. Unzip the file you just downloaded and open the folder you unzipped it to.
3. In the `src` folder, create `weather_token.txt` and paste in your [weatherapi.com token](#obtaining-a-weatherapicom-token). **Make sure to not add an extra line at the start or end. The file should <ins>only</ins> contains the token.**
4. In the `src` folder, create `discord_token.txt` and paste in your [Discord bot token](#obtaining-a-discord-bot-token). **Make sure to not add an extra line at the start or end. The file should <ins>only</ins> contains the token.**
5. In the `src` folder, create `beta_testers.txt` and add certain Discord User's ID into the file, sperated by a new line.
6. Create a new virtual environment with Python by running `python -m venv .venv/` in a terminal.
7. Activate the vitual environment. *(See [this page](https://docs.python.org/3/library/venv.html#how-venvs-work) for how to do that.)*
8. Download the required packages by running `pip install -r requirements.txt`.
9. Move your terminal to be in the `src` folder with `cd src`.
9. Run the bot by running `python main.py`.

## Need help?

Feel free to contact me!

- [Discord Server](https://discord.gg/UKVMvUG2h9)