import requests


# 🔑 Put your real API keys here

GROQ_API_KEY = "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"
SERPAPI_KEY = "6310ff2713922246dfb5421f4ff661fba3baacc2e7f46d6e8a123a915f65439e"




# Function to get related news articles using SerpAPI
def get_related_news(query: str):
    url = f"https://serpapi.com/search.json?q={query}&hl=en&gl=us&api_key={SERPAPI_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        return []
    results = response.json()
    return [item.get("title", "") for item in results.get("organic_results", [])]

# Function to detect fake news using Groq
def detect_fake_news(news_text: str) -> str:
    related_news = get_related_news(news_text)

    context = " ".join(related_news) if related_news else "No related news found."
    prompt = f"""
    Determine if the following news is REAL or FAKE.

    News: {news_text}

    Related News: {context}

    Answer with only one word: REAL or FAKE
    """

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        return "Error contacting Groq API"

    return response.json()["choices"][0]["message"]["content"].strip()

