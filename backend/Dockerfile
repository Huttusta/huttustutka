#syntax=docker/dockerfile:1

FROM python:3.10-slim-bullseye

WORKDIR /app

COPY requirements.txt requirements.txt
RUN apt-get update && apt-get install -y build-essential git libffi-dev rustc libssl-dev
RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .

EXPOSE 5000
ENV FLASK_ENV=production

CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0"]
