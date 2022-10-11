FROM python:latest

# Update default packages
RUN apt-get update

# Get Ubuntu packages
RUN apt-get install -y \
    build-essential \
    curl \
    gcc \
    python3-dev

# Update new packages
RUN apt-get update

# Get Rust
RUN curl https://sh.rustup.rs -sSf | bash -s -- -y

ENV PATH="/root/.cargo/bin:${PATH}"

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
