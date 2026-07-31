# Market.PY Setup Guide

This guide explains how to install, configure, and run Market.PY.

## Requirements

Before starting, make sure you have:

- Python 3.10 or newer
- A Discord account
- A Discord application with a bot created
- Required API keys

## 1. Clone the Repository

```bash
git clone <repository-url>
cd Market.PY
```

## 2. Install Dependencies

Install all required Python packages from `requirements.txt`.

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

## 3. Create a Discord Bot

1. Go to the Discord Developer Portal.
2. Create a new application.
3. Open the **Bot** section.
4. Create a bot user.
5. Copy the bot token.
6. Enable the required intents if needed.
7. Invite the bot to your server with the required permissions.

## 4. Configure API Keys

Market.PY requires external services for market data, news, search, and AI features.

Required services may include:

- Discord Bot Token
- Twelve Data API
- Alpha Vantage API
- GNews API
- Tavily API
- LLM provider API key

Add your keys to the configuration method used by the project.

Example:

```python
DISCORD_TOKEN = "your_token_here"
API_KEY = "your_api_key_here"
```

Do not share your API keys publicly.

## 5. Running the Bot

Start the bot with:

```bash
python main.py
```

or:

```bash
python3 main.py
```

If successful, the bot should log in and become available in your Discord server.

## Troubleshooting

### Bot does not start

Check that:

- Python is installed correctly
- Dependencies were installed
- The Discord token is valid
- API keys are configured correctly

### Commands do not appear

Check that:

- The bot was invited with the correct permissions
- Slash commands are enabled
- The bot is connected to the correct server

### API errors

Most API errors are caused by:

- Missing API keys
- Invalid keys
- API rate limits
- Incorrect configuration

Verify your credentials before reporting an issue.

## Development Notes

Market.PY depends on external APIs and services. A fresh installation requires configuration before it can run.
