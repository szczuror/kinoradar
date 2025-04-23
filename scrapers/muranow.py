import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List
import json
import os
from pathlib import Path

from classes.Movie import Movie


class MuranowScraper:
    def __init__(self):
        self.config = self._load_config()
        self.base_url = self.config["url"]
        self.headers = {'User-Agent': 'Mozilla/5.0'}

    def _load_config(self):
        config_path = Path(__file__).parent.parent / 'data' / 'cinemas.json'
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)["Kino Muranów"]

    def scrape(self) -> List[Movie]:
        soup = self._get_html()
        if not soup:
            return []

        movies = []
        for film in soup.select(self.config["selectors"]["film_container"]):
            title = self._clean_title(film.select_one(self.config["selectors"]["title"]).text)
            screenings = self._get_screenings(film)

            if screenings:
                movies.append(Movie(
                    title=title,
                    source="Kino Muranów",
                    nearest_screening_date=screenings[0]["date"],
                    nearest_screening_time=screenings[0]["time"]
                ))

        return movies

    def _get_html(self):
        try:
            response = requests.get(self.base_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            print(f"Error scraping Muranów: {e}")
            return None

    def _get_screenings(self, film_element) -> list:
        screenings = []
        today = datetime.now()

        for screening in film_element.select(self.config["selectors"]["screening_container"]):
            date_str = screening.select_one(self.config["selectors"]["date"]).text.strip()
            time_str = screening.select_one(self.config["selectors"]["time"]).text.strip()

            try:
                screening_date = datetime.strptime(f"{date_str} {time_str}", "%d.%m.%Y %H:%M")
                if screening_date > today:
                    screenings.append({
                        "date": screening_date.strftime("%Y-%m-%d"),
                        "time": screening_date.strftime("%H:%M")
                    })
            except ValueError:
                continue

        return sorted(screenings, key=lambda x: x["date"])

    def _clean_title(self, title: str) -> str:
        return title.replace("\n", " ").strip()