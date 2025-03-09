FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

RUN uv --version

ENV UV_COMPILE_BYTECODE=1

ADD . /app/

WORKDIR /app/

RUN uv sync --frozen

CMD [ "uv", "run", "roam-bot", "start" ]
