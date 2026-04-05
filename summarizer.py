import os
from groq import Groq

api_key = os.environ.get("GROQ_API_KEY")

client = Groq(api_key=api_key) if api_key else None


def generate_ai_summary(text, region, country):

    if not client:
        return "⚠️ AI summary unavailable (API key missing)"

    prompt = f"""
    You are a power sector analyst.

    Summarize the following transmission news from {region} into 3 bullet points.

    Focus on:
    - Major projects
    - Investments
    - Grid expansion

    Keep each point under 15 words.

    News:
    {text}
    """

    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile"
        )

        return chat_completion.choices[0].message.content.strip()

    except Exception as e:
        print("AI ERROR:", e)
        return "⚠️ AI summary failed"