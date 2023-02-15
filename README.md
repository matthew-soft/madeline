# PROJECT DISCONTINUED!

Hey @everyone,

Sadly, due to big load of overtime work for me (@SanityZeroPercent) in my office. I personally don't have time to maintain the bot anymore. 

So, I'm retiring this repository as PUBLIC REPOSITORY and giving @everyone a big oppoturnity to contribute for the bot source codes.

Enjoy it!

### F.A.Q

Q: Will Madeline be deleted?

A: No, it will most likely be offline.

Q: What happened to the bot then?

A: It will be offline 'till idk when, sorry.

---

# Madeline : The Discord Bot

| Build Production CI | pre-commit CI |
| :---: | :---: |
|  [![Build Production](https://github.com/madeline-bot/madeline/actions/workflows/build.yml/badge.svg)](https://github.com/madeline-bot/madeline/actions/workflows/build.yml)|  [![precommit-action](https://github.com/madeline-bot/madeline/actions/workflows/pre-commit.yml/badge.svg)](https://github.com/madeline-bot/madeline/actions/workflows/pre-commit.yml)  |
-------------------------------------------------
A Multifunctional SA-MP Discord Bot written in [NAFF](https://github.com/NAFTeam/NAFF) (python).

Visit [the official guide](https://naff.info/Guides/01%20Getting%20Started.html) to get started.

## Environment Variables

> Some Keys are need to be provided in ".env" file, and some aren't. Please read this entirely so you didn't do anything wrong :) (~~or just cowabunga and replicate the "example.env" to ".env" and fill the required field.~~)

Some "secrets" are required for the bot to run properly. Here's what you need:

- Discord token = get it from https://discordapp.com/developers/applications/

- Google Cloud Vision Key = You need a Google Cloud Vision Key, which you can get [here](https://cloud.google.com/vision). The key is JSON Formatted, All you have to do is put your (json) key to the root folder and give exact name "gcp-key.json"

- mongodb url = get yourself a free/paid/self-hosted mongodb database and link your project.

- Sentry DSN = To make your bot environment "hassle-free", you should add sentry.io to your project, which is all you need to do is provide the DSN URL. Just create a sentry.io new account, create a new project, and link your project to your bot.

- openweathermap token = Get your OWM token from [here](https://openweathermap.org/api)

- top.gg token = assuming your bot is already published on top.gg, just provide the token.

## Running the Application
There are multiple ways to launch the application.

### Python
To start the bot with python, you first need to install the required packages with
``` bash
pip install -r requirements.txt
```


Then, run:

```bash
python main.py
```


### Docker-Compose
You can use the pre-made docker-compose by running:

```bash
docker-compose up
```

### Docker
For most users, the use of `docker-compose` is highly recommended.

Nevertheless, you can import the pre-made Dockerfile into your own docker-compose or run it manually by with:

```bash
docker build -t madeline .

docker run -it madeline
```

Note: Make sure that you created a volume so that you local `./logs` folder gets populated.

## Additional Information
Additionally, this comes with a pre-made [pre-commit](https://pre-commit.com) config to keep your code clean.

It is recommended that you set this up by running:

```bash
pip install pre-commit

pre-commit install
```
