import re
import time
import groq
import discord
import requests
from tavily import TavilyClient
from duckduckgo_search import DDGS

groq_API = "insert"
discord_TOKEN = "instert"
twelve_API = "insert"
alphaAD_API = "insert"
gNews_API = "insert"
tavily_API = "insert"

groq_client = groq.Groq(api_key=groq_API)

tavily_client = None
if tavily_API and not tavily_API.startswith("tvly-YOUR"):
    try:
        tavily_client = TavilyClient(api_key=tavily_API)
    except Exception as e:
        print(f"[Init Warning] Tavily client failed: {e}")

ticker_aliases = {
    "APPL": "AAPL",
    "APPLE": "AAPL",
    "TESLA": "TSLA",
    "MICROSOFT": "MSFT",
    "GOOGLE": "GOOGL",
    "BITCOIN": "BTC",
    "ETHEREUM": "ETH",
    "NVIDIA": "NVDA",
    "AMAZON": "AMZN",
    "META": "META",
    "SOLANA": "SOL"
}

crypto_symbols = {"BTC", "ETH", "SOL", "DOGE", "XRP", "ADA", "AVAX", "DOT"}


def fix_ticker(symbol):
    symbol = symbol.upper()
    if symbol in ticker_aliases:
        return ticker_aliases[symbol]
    return symbol


def detect_ticker_in_text(text):
    words = re.findall(r'\b[A-Za-z0-9]+\b', text.upper())
    for word in words:
        if word in ticker_aliases:
            return ticker_aliases[word]
        if word in crypto_symbols or (len(word) <= 5 and word.isupper()):
            if word in ["AAPL", "TSLA", "MSFT", "GOOGL", "NVDA", "AMZN", "META", "BTC", "ETH", "SOL"]:
                return word
    return None


def clean_response(text):
    if len(text) > 1700:
        text = text[:1700]

    if text and text[-1] not in ".!?\":)":
        match = re.search(r"^.*[.!?]", text, re.DOTALL)
        if match:
            text = match.group(0)

    return text.strip()


def extract_logs_flag(text):
    pattern = r'--LOGS\b'
    show_logs = bool(re.search(pattern, text, re.IGNORECASE))
    clean_text = re.sub(pattern, '', text, flags=re.IGNORECASE).strip()
    return clean_text, show_logs


def perform_live_web_search(user_query, logs_list):
    enforced_query = f"{user_query} current latest 2026 specs price official"
    logs_list.append(f"🔍 [Search Engine 2026] Executing query: '{enforced_query}'")
    search_context = []
    
    if tavily_client:
        try:
            start_time = time.time()
            res = tavily_client.search(query=enforced_query, max_results=4)
            elapsed = round(time.time() - start_time, 2)
            results = res.get("results", [])
            
            if results:
                logs_list.append(f"✅ [Tavily API] Success in {elapsed}s | Retrieved {len(results)} fresh sources")
                for item in results:
                    search_context.append(f"Title: {item.get('title')}\nSnippet: {item.get('content')}\nURL: {item.get('url')}")
                    logs_list.append(f"  • Source: {item.get('title')} ({item.get('url')})")
                return "\n\n".join(search_context)
            else:
                logs_list.append("⚠️ [Tavily API] 0 results returned. Trying DuckDuckGo...")
        except Exception as e:
            logs_list.append(f"❌ [Tavily API] Error: {e}. Trying DuckDuckGo...")
    else:
        logs_list.append("ℹ️ [Tavily API] Client unconfigured. Using DuckDuckGo...")

    try:
        start_time = time.time()
        ddg_results = list(DDGS().text(enforced_query, max_results=4))
        elapsed = round(time.time() - start_time, 2)
        
        if ddg_results:
            logs_list.append(f"✅ [DuckDuckGo API] Success in {elapsed}s | Retrieved {len(ddg_results)} fresh sources")
            for item in ddg_results:
                search_context.append(f"Title: {item.get('title')}\nSnippet: {item.get('body')}\nURL: {item.get('href')}")
                logs_list.append(f"  • Source: {item.get('title')} ({item.get('href')})")
            return "\n\n".join(search_context)
        else:
            logs_list.append("⚠️ [DuckDuckGo API] 0 results returned.")
    except Exception as e:
        logs_list.append(f"❌ [DuckDuckGo API] Error: {e}")

    return "No live web context retrieved."


def get_price(symbol, logs_list):
    query_symbol = f"{symbol}/USD" if symbol in crypto_symbols else symbol
    logs_list.append(f"📈 [Twelve Data] Fetching price for {query_symbol}")

    try:
        response = requests.get(
            "https://api.twelvedata.com/price",
            params={"symbol": query_symbol, "apikey": twelve_API},
            timeout=5
        )
        data = response.json()
        price = data.get("price", "Unavailable")
        logs_list.append(f"  • Price: {price}")
        return {"symbol": symbol, "price": price}
    except Exception as e:
        logs_list.append(f"❌ [Twelve Data] Failed: {e}")
        return {"symbol": symbol, "price": "Unavailable"}


def get_alpha_news(symbol, logs_list):
    logs_list.append(f"📰 [Alpha Vantage] Fetching news for {symbol}")

    try:
        response = requests.get(
            "https://www.alphavantage.co/query",
            params={"function": "NEWS_SENTIMENT", "tickers": symbol, "apikey": alphaAD_API},
            timeout=5
        )
        data = response.json()
        news = []
        for item in data.get("feed", [])[:2]:
            news.append({"title": item.get("title"), "summary": item.get("summary")})
        logs_list.append(f"  • Articles: {len(news)}")
        return news
    except Exception as e:
        logs_list.append(f"❌ [Alpha Vantage] Failed: {e}")
        return []


def get_gnews(symbol, logs_list):
    logs_list.append(f"🌐 [GNews] Fetching extra news for {symbol}")

    try:
        response = requests.get(
            "https://gnews.io/api/v4/search",
            params={"q": f"{symbol} market", "token": gNews_API, "lang": "en", "max": 2},
            timeout=5
        )
        data = response.json()
        news = []
        for item in data.get("articles", [])[:2]:
            news.append({"title": item.get("title"), "description": item.get("description")})
        logs_list.append(f"  • Articles: {len(news)}")
        return news
    except Exception as e:
        logs_list.append(f"❌ [GNews] Failed: {e}")
        return []


bot = discord.Bot()


@bot.event
async def on_ready():
    print("==============================")
    print(f"✅ Market.PY online as {bot.user}")
    print("Commands:", [cmd.name for cmd in bot.commands])
    print("==============================")


@bot.slash_command(
    name="analyze",
    description="Analyze stock/crypto using live 2026 data. Add --LOGS for execution details."
)
async def analyze(ctx, symbol: str):
    await ctx.defer()
    logs = []

    clean_symbol, show_logs = extract_logs_flag(symbol)
    old_symbol = clean_symbol.upper()
    resolved_symbol = fix_ticker(clean_symbol)

    if old_symbol != resolved_symbol:
        logs.append(f"🔀 [Ticker Resolution] Corrected '{old_symbol}' -> '{resolved_symbol}'")

    logs.append(f"🚀 [Analyze Command] Processing request for: {resolved_symbol}")

    try:
        price_data = get_price(resolved_symbol, logs)
        alpha_news = get_alpha_news(resolved_symbol, logs)
        gnews_data = get_gnews(resolved_symbol, logs)

        web_query = f"{resolved_symbol} stock crypto current market status news"
        live_web_context = perform_live_web_search(web_query, logs)

        logs.append("🤖 [Groq API] Generating response via openai/gpt-oss-120b...")
        start_llm = time.time()

        response = groq_client.chat.completions.create(

            model="llama-3.3-70b-versatile",
            max_tokens=450,
            messages=[
                {
                    "role": "system",
                    "content": """
You are Market.PY, a sharp, conversational financial market bot on Discord.

TEMPORAL ANCHOR: THE CURRENT YEAR IS STRICTLY 2026.

STRICT LAWS:
1. MANDATORY 2026 ACCURACY: Treat all products already released (such as the iPhone 17 series or Xiaomi 17 series) as officially launched. DO NOT frame current post-launch tech as "rumors" or "leaks".
2. SINGLE MESSAGE & SPEECH COMPLETION: Always complete your thoughts fully. Your final sentence MUST end cleanly with proper punctuation (. ! ?).
3. GROUNDING & DATA ACCURACY: Rely strictly on the provided Price Data, API News Data, and Live Web Search Context. Never state outdated training-memory facts.
4. LANGUAGE MATCH: Always reply in the exact same language as the user's input/context.
5. FORMAT: Write natural, conversational chat paragraphs. NEVER use markdown tables or bullet points.
6. DISCLAIMER: End briefly with a friendly reminder that you are an AI Python bot, not financial advice.
"""
                },
                {
                    "role": "user",
                    "content": f"""
Analyze {resolved_symbol}.

Financial API Data:
- Price Data: {price_data}
- News Data: {alpha_news}
- Extra News Data: {gnews_data}

Live Web Context:
{live_web_context}
"""
                }
            ]
        )

        llm_duration = round(time.time() - start_llm, 2)
        logs.append(f"✅ [Groq API] Completed in {llm_duration}s")

        raw_answer = response.choices[0].message.content
        answer = clean_response(raw_answer)

        if old_symbol != resolved_symbol:
            answer = f"Note: Corrected ticker to {resolved_symbol}.\n\n" + answer

        if show_logs:
            log_block = "\n\n```text\n--- EXECUTION LOGS ---\n" + "\n".join(logs) + "\n```"
            answer = answer + log_block

        await ctx.followup.send(answer)

    except Exception as e:
        await ctx.followup.send(f"❌ Error: {e}")


@bot.slash_command(
    name="ask",
    description="Ask Market.PY anything with guaranteed 2026 web search. Add --LOGS for execution details."
)
async def ask(ctx, question: str):
    await ctx.defer()
    logs = []

    clean_question, show_logs = extract_logs_flag(question)
    logs.append(f"🚀 [Ask Command] Processing prompt: '{clean_question}'")

    try:
        detected_symbol = detect_ticker_in_text(clean_question)
        market_api_context = "No specific ticker detected for direct API price fetch."

        if detected_symbol:
            logs.append(f"🎯 [Ticker Detected] Found ticker '{detected_symbol}' in question")
            p_data = get_price(detected_symbol, logs)
            n_data = get_alpha_news(detected_symbol, logs)
            market_api_context = f"Direct Market API Context for {detected_symbol}: Price={p_data}, News={n_data}"

        live_web_context = perform_live_web_search(clean_question, logs)

        logs.append("🤖 [Groq API] Generating response via openai/gpt-oss-120b...")
        start_llm = time.time()

        response = groq_client.chat.completions.create(
            model="openai/gpt-oss-120b",
            max_tokens=450,
            messages=[
                {
                    "role": "system",
                    "content": """
You are Market.PY, a conversational Discord chatbot who loves crypto, stocks, and technology.

TEMPORAL ANCHOR: THE CURRENT YEAR IS STRICTLY 2026.

RESPONSE LAWS:
1. 2026 REALITY CHECK: Devices launched in late 2025/early 2026 (e.g. iPhone 17 series, Xiaomi 17 Ultra) are officially released hardware. Never refer to them as "upcoming rumors" or "unannounced leaks".
2. MANDATORY LIVE GROUNDING: Always answer using the provided Live Web Context and Market API Context. NEVER guess, estimate, or state product releases or specs from old internal training memory.
3. SPEECH COMPLETION & SINGLE MESSAGE: Always complete your speech fully. The final sentence MUST end cleanly on a finished thought with proper punctuation (. ! ?).
4. MULTI-LANGUAGE: Reply in the exact same language as the user's question.
5. NO TABLES OR BULLET LISTS: Write purely in natural, conversational paragraphs.
6. DISCLAIMER: End with a brief note that you are an AI Python bot, not financial advice.
"""
                },
                {
                    "role": "user",
                    "content": f"""
User Question: {clean_question}

Direct Market API Context:
{market_api_context}

Live Web Search Context:
{live_web_context}
"""
                }
            ]
        )

        llm_duration = round(time.time() - start_llm, 2)
        logs.append(f"✅ [Groq API] Completed in {llm_duration}s")

        raw_answer = response.choices[0].message.content
        answer = clean_response(raw_answer)

        if show_logs:
            log_block = "\n\n```text\n--- EXECUTION LOGS ---\n" + "\n".join(logs) + "\n```"
            answer = answer + log_block

        await ctx.followup.send(answer)

    except Exception as e:
        await ctx.followup.send(f"❌ Error: {e}")


print("Starting Market.PY...")
bot.run(discord_TOKEN)