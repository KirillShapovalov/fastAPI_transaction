FROM python:3.10
WORKDIR  /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY  . .
CMD ['uvicorn', 'server:app', ' --host=0.0.0.0', '--reload']