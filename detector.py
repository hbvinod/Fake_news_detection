import requests

# 🔑 Paste your keys hereimport os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

#GROQ_API_KEY = "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"
#SERPAPI_KEY = "6310ff2713922246dfb5421f4ff661fba3baacc2e7f46d6e8a123a915f65439e"


# ---------------------- Functions ----------------------

def fetch_news_from_serpapi(query):
    """Fetch top related news headlines using SerpAPI (Google News)."""
    url = "https://serpapi.com/search"
    params = {"engine": "google_news", "q": query, "api_key": SERPAPI_KEY}
    response = requests.get(url, params=params)

    try:
        data = response.json()
    except Exception:
        return []

    return data.get("news_results", [])[:5]  # return top 5 results


def check_with_groq(news_headline, related_news):
    """Ask Groq to classify news as REAL or FAKE, with explanation."""
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    if not related_news:
        related_text = "(No related sources found in Google News)"
    else:
        related_text = "\n".join([f"- {r['title']} ({r.get('link','')})" for r in related_news])

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a strict fact-checking assistant.\n"
                    "Classify the news headline as either:\n"
                    " - REAL (if it matches or is supported by related headlines)\n"
                    " - FAKE (if it is not supported or seems fabricated)\n\n"
                    "If REAL: mention the most relevant sources and explain briefly why it is real.\n"
                    "If FAKE: explain clearly why it is fake.\n\n"
                    "Output format:\n"
                    "\n \n Verdict: ✅ REAL or \n ❌FAKE\n"
                    "\n Explanation: ...\n"
                    "Sources: (if REAL, list top matching sources)"
                )
            },
            {
                "role": "user",
                "content": f"News headline: {news_headline}\n\nRelated trusted headlines:\n{related_text}"
            }
        ],
        "max_tokens": 512
    }

    response = requests.post(url, headers=headers, json=payload)

    try:
        data = response.json()
    except Exception:
        return f"❌ Invalid Groq response: {response.text}"

    if "choices" in data:
        return data["choices"][0]["message"]["content"]
    else:
        return f"❌ Groq API Error: {data}"


def detect_fake_news(news_headline):
    """Main pipeline: fetch news, then check with Groq."""
    related = fetch_news_from_serpapi(news_headline)
    verdict = check_with_groq(news_headline, related)
    return verdict, related


# ---------------------- Terminal App ----------------------

def main():
    print("\n📰 Fake News Detector ")
    print("----------------------------------------")

    headline = input("\nEnter a news headline to check: ").strip()

    if not headline:
        print("⚠️ Please enter a valid headline.")
        return

    print("\n🔎 Analyzing news credibility... Please wait...\n")

    verdict, sources = detect_fake_news(headline)

    print("📊Result")
    print(verdict)

    if sources:
        print("\n🔗 Related Sources (Google News):")
        for src in sources:
            print(f"- {src['title']} ({src.get('link','')})")


if __name__ == "__main__":
    main()
