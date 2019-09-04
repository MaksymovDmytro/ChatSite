FROM python:3.7

# Does not allows python to buffer output
ENV PYTHONUNBUFFED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# A directory where we are going to store the app
RUN mkdir /app
WORKDIR /app

# Copy anythign from local app folder to docker container app folder
COPY ./app /app

#RUN         apt-get update && apt-get install -y redis-server
#EXPOSE      6379
#ENTRYPOINT  ["/usr/bin/redis-server"]