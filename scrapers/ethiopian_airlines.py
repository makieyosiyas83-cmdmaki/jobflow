import hashlib
import re
from datetime import date
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from dateutil import parser as date_parser

SOURCE_URL = "https://corporate.ethiopianairlines.com/AboutEthiopian/careers/vacancies"

def parse_date(text):
    try:
        return date_parser.parse(text, fuzzy=True).date().isoformat()
    except Exception:
        return None

def scrape_ethiopian_airlines():
    response = requests.get(SOURCE_URL, timeout=30, headers={"User-Agent": "JobFlow job collector"})
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    jobs, seen = [], set()

    for link in soup.find_all("a", href=True):
        title = " ".join(link.get_text(" ", strip=True).split())
        url = urljoin(SOURCE_URL, link["href"])
        if not title or len(title) < 4 or url in seen:
            continue
        parent = link.parent
        context = " ".join(parent.get_text(" ", strip=True).split()) if parent else title
        lower = context.lower()
        if not any(word in lower for word in ("vacan", "career", "position", "deadline", "register", "job")):
            continue

        deadline = None
        match = re.search(r"(?:deadline|closing|registration period)[^\n]{0,100}", context, re.I)
        if match:
            deadline = parse_date(match.group(0))
        if deadline and date.fromisoformat(deadline) < date.today():
            continue

        seen.add(url)
        external_id = hashlib.sha256(f"ethiopian_airlines|{title}|{url}".encode()).hexdigest()
        jobs.append({
            "external_id": external_id,
            "title": title,
            "company": "Ethiopian Airlines",
            "location": "Ethiopia",
            "description": context,
            "deadline": deadline,
            "source_name": "Ethiopian Airlines",
            "source_url": url,
            "status": "active"
        })
    return jobs
