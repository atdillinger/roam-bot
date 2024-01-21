FROM python:3.10

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt # refactor; seperate requirements for dev and container

COPY stagings.yml .
COPY src/* .
RUN chmod +x main.py
 
CMD [ "python", "main.py", "start" ]