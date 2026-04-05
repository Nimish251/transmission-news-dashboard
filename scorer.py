def is_relevant(title):
    title_lower = title.lower()

    strong_keywords = [
        "transmission line", "hvdc", "substation",
        "grid expansion", "interconnector",
        "grid upgrade", "grid modernization",
        "power transmission", "electric grid"
    ]

    tso_keywords = [
        "tennet", "amprion", "50hertz", "transnetbw",
        "rte", "terna", "ree", "pse", "apg",
        "national grid", "pgcil", "power grid",
        "aemo", "transgrid",
        "pjm", "ercot", "hydro quebec",
        "eskom", "ons", "cammesa"
    ]

    if any(k in title_lower for k in strong_keywords):
        return True

    if any(t in title_lower for t in tso_keywords):
        return True

    return False


def get_importance_score(title):
    title_lower = title.lower()
    score = 0

    keyword_scores = {
        "hvdc": 6,
        "interconnector": 6,
        "765 kv": 5,
        "500 kv": 5,
        "400 kv": 4,
        "substation": 3,
        "transmission line": 5,
        "grid expansion": 4,
        "grid upgrade": 4,
        "grid modernization": 4,
        "approved": 3,
        "commissioned": 4,
        "energized": 4,
        "awarded": 4,
        "tender": 4,
        "investment": 3,
        "billion": 3,
        "million": 1
    }

    for k, v in keyword_scores.items():
        if k in title_lower:
            score += v

    return score


def extract_country(title):
    title_lower = title.lower()

    country_map = {
        # EUROPE (expanded)
        "germany": "Germany", "france": "France", "italy": "Italy",
        "spain": "Spain", "poland": "Poland", "austria": "Austria",
        "netherlands": "Netherlands", "belgium": "Belgium",
        "sweden": "Sweden", "norway": "Norway", "finland": "Finland",
        "denmark": "Denmark", "switzerland": "Switzerland",
        "portugal": "Portugal", "greece": "Greece",
        "czech": "Czech Republic", "hungary": "Hungary",
        "romania": "Romania", "bulgaria": "Bulgaria",
        "uk": "UK", "united kingdom": "UK",

        # ASIA
        "india": "India", "china": "China", "japan": "Japan",
        "south korea": "South Korea", "indonesia": "Indonesia",
        "vietnam": "Vietnam", "thailand": "Thailand",
        "malaysia": "Malaysia", "philippines": "Philippines",

        # AFRICA
        "south africa": "South Africa", "egypt": "Egypt",
        "kenya": "Kenya", "nigeria": "Nigeria",
        "morocco": "Morocco", "algeria": "Algeria",

        # MIDDLE EAST
        "uae": "UAE", "saudi": "Saudi Arabia",
        "qatar": "Qatar", "oman": "Oman", "kuwait": "Kuwait",

        # AMERICAS
        "usa": "USA", "united states": "USA", "canada": "Canada",
        "brazil": "Brazil", "argentina": "Argentina",
        "chile": "Chile", "mexico": "Mexico", "peru": "Peru",

        # OCEANIA
        "australia": "Australia", "new zealand": "New Zealand"
    }

    tso_country_map = {
        "tennet": "Netherlands",
        "amprion": "Germany",
        "50hertz": "Germany",
        "transnetbw": "Germany",
        "rte": "France",
        "terna": "Italy",
        "ree": "Spain",
        "pse": "Poland",
        "apg": "Austria",
        "national grid": "UK",
        "pgcil": "India",
        "aemo": "Australia",
        "pjm": "USA",
        "ercot": "USA",
        "hydro quebec": "Canada",
        "eskom": "South Africa",
        "ons": "Brazil",
        "cammesa": "Argentina"
    }

    for k, v in country_map.items():
        if k in title_lower:
            return v

    for k, v in tso_country_map.items():
        if k in title_lower:
            return v

    return "Global"