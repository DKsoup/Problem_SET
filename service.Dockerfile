# Use the official python3.8-slim as the base image
FROM python:3.8-slim

# Author
MAINTAINER ZYL

# Setting up the working directory
WORKDIR /usr/src/server

# Copy the contents of the current directory to the working directory
COPY . /usr/src/server

# Install flask open source framework
RUN mkdir -p /usr/src/server/log/ \
    && pip install flask

# Set the environment variable to specify the log file path
ENV LOG_FILE=/usr/src/server/log/service.log

# Running Flask
ENTRYPOINT ["python", "service.py"]