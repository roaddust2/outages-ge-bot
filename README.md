![Python](https://img.shields.io/badge/python-v3.11-blue)
[![Deploy](https://github.com/roaddust2/outages-ge-bot/actions/workflows/deploy.yml/badge.svg)](https://github.com/roaddust2/outages-ge-bot/actions/workflows/deploy.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/12af23439b2959845c8e/maintainability)](https://codeclimate.com/github/roaddust2/outages-ge-bot/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/12af23439b2959845c8e/test_coverage)](https://codeclimate.com/github/roaddust2/outages-ge-bot/test_coverage)
# outages-ge-bot

## About
It is an app written in Python with the aiogram framework. This bot will assist you with information about the latest outages in Georgia (the country).

## Stack
- Python 3.11
- Aiogram 3.0.0rc1

## Roadmap
### 0.1.x
- [x] Basic notifier functionality
- [x] Ability to save up to 2 addresses
- [x] Ability to list and remove addresses
- [x] Tbilisi support [GWP, Telasi]
### 0.2.x
- [ ] Batumi support
- [ ] Kutaisi support
- [ ] \(Optional) Mobile providers support [Magti, Silknet etc.]
### 0.3.x
- [ ] Manage subscriptions to specific providers (on/off) through dialog

## Installation (with Docker)
### Variables

  ```.env
  API_TOKEN=your_telegram_api_token

  DB_HOST=postgres
  DB_PORT=5435
  DB_NAME=postgres
  DB_USER=postgres
  DB_PASSWORD=password

  # Necessary for postgresql image
  POSTGRES_DB=postgres
  POSTGRES_PASSWORD=password
  POSTGRES_USER=postgres
  ```
### Steps

  ```bash
  # Clone the repository and install dependencies
  git clone git@github.com:roaddust2/outages-ge-bot.git
  cd outages-ge-bot

  # Create .env file and add environment variables
  touch .env

  # Run container
  docker compose up 
  ```

## Installation (with Poetry)
### Variables

  ```.env
  API_TOKEN=your_telegram_api_token

  DB_HOST=postgres
  DB_PORT=5432
  DB_NAME=postgres
  DB_USER=postgres
  DB_PASSWORD=password
  ```
### Steps

  ```bash
  # Clone the repository and install dependencies
  git clone git@github.com:roaddust2/outages-ge-bot.git
  cd outages-ge-bot
  make setup
  
  # Create basic PostgreSQL database
  
  # Create .env file and add environment variables
  touch .env
  
  # Apply alembic migrations
  make alembic-upgrade
  
  # Start application
  make start
  ```
