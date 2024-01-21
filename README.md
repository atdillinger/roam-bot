# Setup

1. Be on Ubuntu
1. Install Python3.10
1. Install python3.10-venv
1. Install make
1. Install docker
1. Run: `export DISCORD_KEY=<bot key>`
1. Run: `make dev`
1. Run: `docker build -t roam-bot-0.0.0 .`
1. Run: `docker run -e DISCORD_KEY=$DISCORD_KEY roam-bot-0.0.0`

## Running Locally

I have implemented `click` commands for each developed `discord.py` command. These can be run locally using:

1. Run: `make dev`
1. Run: `export DISCORD_KEY=<bot key>`
1. Run: `./src/main.py thera-local`
1. Run: `./src/main.py jita-local`
1. Run: `./src/main.py roam-local`
