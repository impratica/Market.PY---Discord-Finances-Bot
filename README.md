# Market.PY

Discord bot for live stock and crypto market analysis using financial APIs and LLMs.

## Features

- Stock and crypto price fetching using Twelve Data
- Financial news integration using Alpha Vantage and GNews
- Live web search context using Tavily and DuckDuckGo fallback
- AI-generated market explanations through LLMs
- Discord slash commands
- Ticker detection and typo correction
- Optional execution logs for debugging

## Commands

### /analyze

Analyzes a stock or cryptocurrency using market data, news, and AI.

Example:

/analyze AAPL

### /ask

Ask Market.PY questions about markets, companies, technology, or finance.

Example:

/ask How is Nvidia performing?

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd Market.PY
```

Install the required dependencies:

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

## Before Reporting Issues

If the bot does not start or commands do not work, verify that the project has been configured correctly.

This project **will not function out of the box**. You must:

* Create a Discord application and bot in the Discord Developer Portal.
* Add your bot to a server with the required permissions.
* Configure all required API keys (such as Twelve Data, Alpha Vantage, GNews, Tavily, and the LLM provider).
* Provide your Discord bot token.
* Set up the required environment variables or configuration file before running the bot.

Most startup issues are caused by missing or invalid API keys, an invalid Discord token, or an incomplete Discord application setup—not by the source code itself.

Please confirm your configuration before opening an issue.

## Known Issues

### Creator Identity Hallucination

Market.PY may incorrectly describe its creator when asked about its origin.

Although explicit creator information is provided to the model, it may occasionally generate false details, such as claiming that Market.PY was created by a fictional "team of developers interested in Python and crypto."

This is a known LLM hallucination issue. The generated response should not be considered a reliable source for project ownership or authorship.

For accurate information, refer to this repository and its documentation.

