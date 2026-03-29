import feedparser
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime

from scorer import is_relevant, get_importance_score, extract_country
from summarizer import generate_ai_summary


def clean_title(title):
    if " - " in title:
        parts = title.rsplit(" - ", 1)
        return parts[0].strip()
    return title.strip()


def extract_source(title):
    if " - " in title:
        parts = title.rsplit(" - ", 1)
        return parts[1].strip()
    return "Unknown Source"


def classify_news(title):
    title_lower = title.lower()

    if any(word in title_lower for word in ["tender", "bid", "award", "awarded", "contract"]):
        return "Tender"
    elif any(word in title_lower for word in ["commissioned", "energized", "operational", "in service"]):
        return "Commissioning"
    elif any(word in title_lower for word in ["investment", "funding", "billion", "million"]):
        return "Investment"
    elif any(word in title_lower for word in ["policy", "approval", "approved", "regulation"]):
        return "Policy"
    else:
        return "Project Update"


def remove_duplicates(news_items):
    seen_titles = set()
    unique_items = []

    for item in news_items:
        normalized_title = item["clean_title"].lower()
        if normalized_title not in seen_titles:
            seen_titles.add(normalized_title)
            unique_items.append(item)

    return unique_items


def is_within_last_30_days(published_text):
    try:
        published_date = parsedate_to_datetime(published_text)

        if published_date.tzinfo is None:
            published_date = published_date.replace(tzinfo=timezone.utc)

        now = datetime.now(timezone.utc)
        cutoff = now - timedelta(days=30)

        return published_date >= cutoff
    except Exception:
        return False


def get_news(limit=5):
    url = "https://news.google.com/rss/search?q=(transmission+line+OR+power+transmission+OR+hvdc+OR+interconnector+OR+substation)&hl=en-IN&gl=IN&ceid=IN:en"

    feed = feedparser.parse(url)
    news_items = []

    for entry in feed.entries:
        original_title = entry.title
        clean_news_title = clean_title(original_title)
        source = extract_source(original_title)
        link = entry.link
        published = getattr(entry, "published", "No date available")

        if not is_within_last_30_days(published):
            continue

        if is_relevant(clean_news_title):
            score = get_importance_score(clean_news_title)
            category = classify_news(clean_news_title)
            country = extract_country(clean_news_title)

            news_items.append({
                "title": original_title,
                "clean_title": clean_news_title,
                "source": source,
                "link": link,
                "published": published,
                "score": score,
                "category": category,
                "country": country
            })

    news_items = remove_duplicates(news_items)
    news_items = sorted(news_items, key=lambda x: x["score"], reverse=True)
    news_items = news_items[:limit]

    for item in news_items:
        item["ai_summary"] = generate_ai_summary(
            item["clean_title"],
            item["category"],
            item["country"]
        )

    return news_items