FROM python:latest
FROM rust:latest

# we want stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# add the path to pythonpath
ENV PYTHONPATH "${PYTHONPATH}:/app"

# install uvloop for faster asyncio
RUN pip install uvloop

# install the requirements
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# copy over the source files
COPY ./ /app/

# start the bot
WORKDIR /app
CMD ["python", "main.py"]
