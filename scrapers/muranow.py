import requests
from bs4 import BeautifulSoup
from classes.Movie import Movie
from typing import List
from collections import defaultdict

def scrape_muranow() -> List[Movie]:
    SRC = 'Kino Muranów'
    URL = "https://kinomuranow.pl/repertuar"

    def fetch_page(url: str) -> BeautifulSoup:
        try:
            response = requests.get(url)
            response.raise_for_status()
            return BeautifulSoup(response.text, "html.parser")
        except requests.RequestException as e:
            print(f"Błąd podczas pobierania strony: {e}")
            return None

    def parse_movies(soup: BeautifulSoup) -> List[Movie]:
        movies_dict = defaultdict(list)
        days = soup.find_all("div", class_="calendar-seance-full__day")

        for day in days:
            if "calendar-seance-full__day--filled" in day.get("class", []):
                date_str = extract_date(day)
                movie_blocks = day.find_all("div", class_="movie-calendar-info")

                for block in movie_blocks:
                    original_title = extract_title(block)
                    if original_title:
                        movies_dict[original_title].append(date_str)

        return [Movie(original_title=title, show_dates=dates, source=SRC) for title, dates in movies_dict.items()]

    def extract_date(day) -> str:
        day_num = day.find("span", class_="cell-date-header__day-num").get_text(strip=True)
        month = day.find("span", class_="cell-date-header__day-month").get_text(strip=True)
        return f"{day_num} {month}"

    def extract_title(block) -> str:
        title_tag = block.find("h5", class_="movie-calendar-info__title")
        return title_tag.get_text(strip=True) if title_tag else None

    soup = fetch_page(URL)
    if soup:
        return parse_movies(soup)
    return []

# Przykład użycia
# if __name__ == "__main__":
#     movies = scrape_muranow()
#     for movie in movies:
#         print(movie)
