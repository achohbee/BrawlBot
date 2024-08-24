# BrawlBot

Installation instructions:

1. Install python, pip, and pipenv
1. Create a local user named brawlbot
1. Clone this repo into /home/brawlbot/bot
1. Create a local pip virtual environment using the Pipfile
1. Create a .env file with DISCORD_TOKEN set appropriately
	```
	DISCORD_TOKEN=.....
	```
1. Copy brawlbot.service to /etc/systemd/system
1. Enable via:
	```
	systemctl enable brawlbot
	```
