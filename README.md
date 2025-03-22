# AccentuAI

FastAPI based text accentuation and correction service using LLMs.

## Setup

Make sure to copy the `.env` file containing the config settings (API key/URL and DB URL) to the root folder of the project.

First install the required version of python as defined in the project (3.12.7) with pyenv:
- install pyenv if necessary: `brew install pyenv` 
- install 3.12.7: `pyenv install 3.12.7`
- set the pyenv version: `pyenv local 3.12.7`

- create python virtual env: `python3 -m venv .venv`
- activate virtual env: `source .venv/bin/activate`
- upgrade pip: `pip install --upgrade pip`
- install dev requirements: `pip install -r requirements-dev.txt`
- install requirements: `pip install -r requirements.txt`

## Running the API

- run the server with: `./run-server.sh`
- use the FastAPI docs page to test the API: http://localhost:8000/docs

## Testing

Run tests in the root folder with `python -m pytest`
