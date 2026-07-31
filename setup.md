# Market.PY Setup Guide

This guide explains how to install, configure, and run Market.PY.

## Requirements

Before running Market.PY, make sure you have:

- Python 3.10 or newer
- A Discord account
- A Discord Developer Application
- Required API keys

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd Market.PY
```

Install all required Python packages:

### Windows

```powershell
py -m pip install -r requirements.txt
```

If `py` is unavailable:

```powershell
python -m pip install -r requirements.txt
```

### Linux

```bash
python3 -m pip install -r requirements.txt
```

### macOS

```bash
python3 -m pip install -r requirements.txt
```

---

# Environment Configuration

Market.PY uses environment variables to store private credentials such as Discord tokens and API keys.

The project includes an `.env.example` file. This file is a template and does not contain real keys.

## Scenario 1: New User Setup

If you downloaded or cloned Market.PY for the first time:

Create your local `.env` file from the template:

```bash
cp .env.example .env
```

Open the new `.env` file and replace the placeholders with your own credentials:

```env
DISCORD_TOKEN=your_discord_token_here
GROQ_API_KEY=your_groq_api_key_here
TWELVE_DATA_API_KEY=your_twelve_data_key_here
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
GNEWS_API_KEY=your_gnews_key_here
TAVILY_API_KEY=your_tavily_key_here
```

You must provide your own API keys. Market.PY does not include any private credentials.

---

## Scenario 2: Developer Setup

If you are developing or testing Market.PY locally:

Create your own `.env` file in the project folder:

```text
Market.PY/
├── marketbot.py
├── README.md
├── SETUP.md
├── requirements.txt
└── .env
```

Your `.env` file should contain your real keys:

```env
DISCORD_TOKEN=your_real_discord_token
GROQ_API_KEY=your_real_groq_key
TWELVE_DATA_API_KEY=your_real_twelve_data_key
ALPHA_VANTAGE_API_KEY=your_real_alpha_vantage_key
GNEWS_API_KEY=your_real_gnews_key
TAVILY_API_KEY=your_real_tavily_key
```

Never upload this file to GitHub.

The `.env` file is only for your local machine.

---

# Creating a Discord Bot

1. Go to the Discord Developer Portal.
2. Create a new application.
3. Open the Bot section.
4. Create a bot user.
5. Copy your bot token.
6. Invite the bot to your Discord server.
7. Give it the required permissions.

---

# API Services

Market.PY uses multiple external services:

## Groq

Used for AI-generated market explanations.

Required:

```text
GROQ_API_KEY
```

## Twelve Data

Used for live stock and cryptocurrency prices.

Required:

```text
TWELVE_DATA_API_KEY
```

## Alpha Vantage

Used for financial news.

Required:

```text
ALPHA_VANTAGE_API_KEY
```

## GNews

Used for additional news sources.

Required:

```text
GNEWS_API_KEY
```

## Tavily

Used for live web search context.

Required:

```text
TAVILY_API_KEY
```

---

# Running Market.PY

Start the bot with:

```bash
python marketbot.py
```

or:

```bash
python3 marketbot.py
```

If the configuration is correct, the bot will connect to Discord and register its commands.

---

# Troubleshooting

## Bot does not start

Check:

- Python version is 3.10+
- Dependencies are installed
- `.env` exists
- Discord token is valid
- API keys are correct

## Slash commands do not appear

Check:

- The bot was invited correctly
- The bot has permission to use applications commands
- The bot is connected to the correct server

## API errors

Common causes:

- Missing API keys
- Invalid API keys
- API rate limits
- Incorrect environment configuration

Verify your `.env` file before reporting issues.

---

# Security

Never upload:

- `.env`
- Discord tokens
- API keys

Only upload:

- `.env.example`
- Source code
- Documentation

Compromised API keys should be revoked immediately.
