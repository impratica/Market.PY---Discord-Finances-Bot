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

## Requirements

Python 3.10+

Install dependencies:

```bash
pip install -r requirements.txt
