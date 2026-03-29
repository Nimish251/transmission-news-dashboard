import os
from groq import Groq

api_key = os.environ.get("GROQ_API_KEY")

client = Groq(api_key=api_key) if api_key else None


def generate_ai_summary(title, category, country):
    if not client:
        return "AI summary unavailable. GROQ_API_KEY not set."

    prompt = f"""
    You are helping build a transmission line news dashboard.
    Summarize this news item in one short sentence.
    Focus on why it matters for transmission, grid, utilities, or power infrastructure.

    Title: {title}
    Category: {category}
    Country: {country}

    Keep the answer under 25 words.
    """

    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile"
        )

        return chat_completion.choices[0].message.content.strip()

    except Exception:
        return "AI summary could not be generated."