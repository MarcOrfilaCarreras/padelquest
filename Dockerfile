FROM ubuntu:20.04

RUN apt-get update && apt-get install --no-install-recommends -y \
    gcc-aarch64-linux-gnu \
    python3-dev \
    python3-pip \
&& rm -rf /var/lib/apt/lists/*

RUN mkdir /app
COPY app /app
COPY requirements.txt /app/requirements.txt
WORKDIR /app

RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn

RUN groupadd -r gunicorn && useradd --no-log-init -r -g gunicorn gunicorn

RUN chown -R gunicorn:gunicorn /app

USER gunicorn

EXPOSE 80

ENTRYPOINT [ "gunicorn" ]
CMD ["--bind", "0.0.0.0:80", "entrypoint:app"]
