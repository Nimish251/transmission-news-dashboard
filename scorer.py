def is_relevant(title):
    title_lower = title.lower()

    strong_keywords = [
        "transmission line",
        "power transmission",
        "electricity transmission",
        "grid expansion",
        "interconnector",
        "substation",
        "hvdc",
        "hvac",
        "transmission project",
        "grid infrastructure",
        "power grid"
    ]

    weak_keywords = [
        "line",
        "grid",
        "transmission",
        "utility",
        "power"
    ]

    if any(keyword in title_lower for keyword in strong_keywords):
        return True

    weak_match_count = sum(1 for keyword in weak_keywords if keyword in title_lower)
    return weak_match_count >= 2


def get_importance_score(title):
    title_lower = title.lower()
    score = 0

    keyword_scores = {
        "hvdc": 5,
        "interconnector": 5,
        "765 kv": 5,
        "500 kv": 4,
        "400 kv": 4,
        "substation": 3,
        "transmission line": 4,
        "transmission project": 4,
        "grid expansion": 3,
        "power grid": 2,
        "approved": 3,
        "commissioned": 3,
        "awarded": 3,
        "tender": 3,
        "investment": 2,
        "billion": 2,
        "million": 1,
        "expansion": 2
    }

    for keyword, points in keyword_scores.items():
        if keyword in title_lower:
            score += points

    return score


def extract_country(title):
    title_lower = title.lower()

    country_map = {
        "india": "India",
        "china": "China",
        "usa": "USA",
        "united states": "USA",
        "canada": "Canada",
        "uk": "UK",
        "united kingdom": "UK",
        "germany": "Germany",
        "france": "France",
        "italy": "Italy",
        "spain": "Spain",
        "poland": "Poland",
        "romania": "Romania",
        "hungary": "Hungary",
        "georgia": "Georgia",
        "azerbaijan": "Azerbaijan",
        "kazakhstan": "Kazakhstan",
        "uzbekistan": "Uzbekistan",
        "kyrgyzstan": "Kyrgyzstan",
        "thailand": "Thailand",
        "vietnam": "Vietnam",
        "malaysia": "Malaysia",
        "indonesia": "Indonesia",
        "philippines": "Philippines",
        "australia": "Australia",
        "brazil": "Brazil",
        "mexico": "Mexico",
        "south africa": "South Africa",
        "egypt": "Egypt",
        "saudi arabia": "Saudi Arabia",
        "uae": "UAE",
        "turkey": "Turkey"
    }

    for keyword, country in country_map.items():
        if keyword in title_lower:
            return country

    return "Global / Unclear"