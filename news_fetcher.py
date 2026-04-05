import feedparser
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from urllib.parse import quote

from scorer import is_relevant, get_importance_score, extract_country
from summarizer import generate_ai_summary


REGION_CONFIG = {
    "India": ["india"],
    "South-East Asia": ["indonesia", "vietnam", "thailand", "malaysia", "philippines"],
    "Europe": ["germany", "france", "italy", "spain", "poland", "netherlands", "uk", "sweden", "norway"],
    "CIS": ["kazakhstan", "uzbekistan", "azerbaijan"],
    "Africa": ["south africa", "egypt", "kenya", "nigeria", "morocco"],
    "Middle-East": ["uae", "saudi arabia", "qatar", "oman"],
    "Australia": ["australia"],
    "North America": ["usa", "canada"],
    "South America": ["brazil", "argentina", "chile", "mexico"]
}


def is_recent(published_text):
    try:
        dt = parsedate_to_datetime(published_text)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)

        return dt >= datetime.now(timezone.utc) - timedelta(days=7)
    except:
        return False


def detect_region(country):
    country_lower = country.lower()

    for region, countries in REGION_CONFIG.items():
        for c in countries:
            if c in country_lower:
                return region

    return "Other"


def remove_duplicates(items):
    seen = set()
    unique = []

    for item in items:
        key = item["title"].lower()
        if key not in seen:
            seen.add(key)
            unique.append(item)

    return unique


def fetch_news():
    all_items = []

    for region, countries in REGION_CONFIG.items():

        query = " OR ".join(countries)
        encoded_query = quote(f"({query}) (transmission OR grid OR substation OR hvdc)")

        url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-IN&gl=IN&ceid=IN:en"

        feed = feedparser.parse(url)

        for entry in feed.entries:
            title = entry.title
            link = entry.link
            published = getattr(entry, "published", "")

            if not is_recent(published):
                continue

            if not is_relevant(title):
                continue

            score = get_importance_score(title)

            if score <= 0:
                continue

            try:
                dt = parsedate_to_datetime(published)
                published_clean = dt.strftime("%d %b %Y")
            except:
                published_clean = "Recent"

            country = extract_country(title)
            region_detected = detect_region(country)

            all_items.append({
                "title": title,
                "link": link,
                "published": published_clean,
                "country": country,
                "region": region_detected,
                "score": score,
                "source": "Google News"
            })

    return remove_duplicates(all_items)


def get_news():
    all_items = fetch_news()

    region_news = {region: [] for region in REGION_CONFIG.keys()}

    for item in all_items:
        region = item["region"]
        if region in region_news:
            region_news[region].append(item)

    final_output = {}

    for region, items in region_news.items():
        if not items:
            continue

        items = sorted(items, key=lambda x: x["score"], reverse=True)[:10]

        combined_text = "\n".join([i["title"] for i in items])

        summary = generate_ai_summary(combined_text, region, "Multiple") if combined_text else "No major updates."

        final_output[region] = {
            "news": items,
            "summary": summary
        }

    return final_output