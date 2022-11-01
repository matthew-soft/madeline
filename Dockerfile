FROM python:3.10.8-bullseye

# Update default packages
RUN apt-get update && apt-get upgrade -y

# we want stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# add the path to pythonpath
ENV PYTHONPATH "${PYTHONPATH}:/app"

# install uvloop for faster asyncio
RUN pip3.10 install uvloop

# install the requirements
COPY ./requirements.txt /app/requirements.txt
RUN pip3.10 install -r /app/requirements.txt

# copy over the source files
COPY ./ /app/

# set the working directory
WORKDIR /app

# Add Google Cloud Credentials to PATH
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/gcp-key.json"

# start the bot
CMD ["python3.10", "main.py"]
