# Setup

1. Install docker
1. Run: `export DISCORD_KEY=<bot key>`
1. Run: `docker run -e DISCORD_KEY=$DISCORD_KEY adilly/roam-bot:0.0.2`

## Running Locally

I have implemented `click` commands for each developed `discord.py` command.

## Local Dev

1. Run: `export DISCORD_KEY=<bot key>`
1. Run: `./src/main.py thera-local`
1. Run: `./src/main.py jita-local`
1. Run: `./src/main.py roam-local`
1. `uv run pytest`
1. `git config --local core.hooksPath .githooks`

## Reference Docs

- [ship destruction tracking via zkillboard](https://github.com/zKillboard/zKillboard/wiki/API-(Killmails))
