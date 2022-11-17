FROM python:3.11.0

# Update default packages
RUN apt-get update && apt-get upgrade -y

# we want stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# add the path to pythonpath
ENV PYTHONPATH "${PYTHONPATH}:/app"

# install uvloop for faster asyncio
RUN pip3.11 install uvloop

# install the requirements
COPY ./requirements.txt /app/requirements.txt
RUN pip3.11 install -r /app/requirements.txt

# copy over the source files
COPY ./ /app/

# set the working directory
WORKDIR /app

# Add Google Cloud Credentials to PATH
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/gcp-key.json"

# start the bot
CMD ["python3.11", "main.py"]
