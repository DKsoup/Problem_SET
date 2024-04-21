# Use the official python3.8-slim image as your base image.
FROM python:3.8-slim

# Author
MAINTAINER ZYL

# Setting up the working directory
WORKDIR /usr/src/client

# Copy the contents of the current directory to the working directory
COPY ./client.py /usr/src/client

# Installing the requests library
RUN mkdir -p /usr/src/client/log/ \
    && pip install requests

# Set the environment variable to specify the log file path
ENV LOG_FILE=/usr/src/client/log/info.log

# Run client
ENTRYPOINT []