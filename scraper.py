# scraper.py
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
import re

# Base URL for Wikipedia tourism pages
BASE_URL = "https://en.wikipedia.org/wiki/Tourism_in_"

# List of destinations (match actual Wikipedia page titles)
DESTINATIONS = [
    "Paris",
    "Tokyo",
    "Rome",
    "Bangkok",
    "New_York_City",
    "London",
    "Barcelona",
    "Dubai"
]

# User-Agent header to avoid bot blocks
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Educational Web Scraper)"
}

def scrape_destination(destination):
    """
    Scrapes destination name and first meaningful paragraph from Wikipedia tourism pages.
    Returns a dictionary with 'destination', 'description', and 'source_url'
    """
    url = BASE_URL + destination
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print(f"Failed to fetch {destination} ({response.status_code})")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # 1️⃣ Destination title
    title_tag = soup.find("h1", id="firstHeading")
    title = title_tag.get_text(strip=True) if title_tag else destination.replace("_", " ")

    # 2️⃣ First meaningful paragraph
    description = "No description available"
    content_div = soup.find("div", class_="mw-parser-output")

    if content_div:
        paragraphs = content_div.find_all("p")
        for p in paragraphs:
            text = p.get_text(strip=True)
            # Skip short/empty paragraphs, navigation notes, or edit tags
            if len(text) > 50 and re.search('[a-zA-Z]', text):
                description = text
                break

    return {
        "destination": title,
        "description": description,
        "source_url": url
    }

def main():
    """
    Scrapes all destinations and saves them to CSV
    """
    scraped_data = []

    for place in DESTINATIONS:
        print(f"Scraping {place}...")
        data = scrape_destination(place)
        if data:
            scraped_data.append(data)
        time.sleep(1)  # polite delay

    # Ensure data folder exists
    os.makedirs("data", exist_ok=True)

    # Save to CSV
    df = pd.DataFrame(scraped_data)
    df.to_csv("data/travel_destinations.csv", index=False)

    print("✅ Scraping completed. Data saved to data/travel_destinations.csv")

if __name__ == "__main__":
    main()
