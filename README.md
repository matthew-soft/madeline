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

# Running the Application
There are multiple ways to launch the application.


### Python
To start the bot with python, you first need to install the required packages with `pip install -r requirements.txt`


Then, run:

1) `python main.py`


### Docker-Compose
You can use the pre-made docker-compose by running:

1) `docker-compose up`

### Docker
For most users, the use of `docker-compose` is highly recommended.

Nevertheless, you can import the pre-made Dockerfile into your own docker-compose or run it manually by with:

1) `docker build -t madeline .`
2) `docker run -it madeline`

Note: Make sure that you created a volume so that you local `./logs` folder gets populated.

# Additional Information
Additionally, this comes with a pre-made [pre-commit](https://pre-commit.com) config to keep your code clean.

It is recommended that you set this up by running:

1) `pip install pre-commit`
2) `pre-commit install`
