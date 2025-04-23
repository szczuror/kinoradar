import requests
from bs4 import BeautifulSoup
from imdb import IMDb # type: ignore
from fuzzywuzzy import fuzz # type: ignore
from imdb import IMDb # type: ignore
import time
import json
import os
import re

start_time = time.time()

# śćieżka do cache
translations_file = 'data/translations.json'

# Inicjalizacja obiektu IMDb
ia = IMDb()

# Funkcja do pobrania listy filmów z Letterboxd na podstawie podanego username
def get_letterboxd_watchlist(username):
    watchlist = []
    page_number = 1

    while True:
        # pobieranie strony
        url = f"https://letterboxd.com/{username}/watchlist/page/{page_number}/"
        response = requests.get(url)

        # Sprawdź, czy strona istnieje
        if response.status_code != 200:
            break

        # Parsuj HTML
        soup = BeautifulSoup(response.text, "html.parser")
        films = soup.find_all("li", class_="poster-container")

        # Jeśli nie ma filmów na stronie, zakończ
        if not films:
            break

        # Dodaj tytuły filmów do watchlisty
        for film in films:
            title = film.find("img")["alt"]
            watchlist.append(title)

        # Przejdź do następnej strony
        page_number += 1

    return watchlist

# Funkcja do pobrania listy filmów z Filmweb (z Warszawy)
def get_filmweb_movies():
    url = 'https://www.filmweb.pl/showtimes/Warszawa'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        movie_links = soup.find_all('a', class_='preview__link')

        filmweb_movies = [link.get_text(strip=True) for link in movie_links]
        return filmweb_movies
    else:
        print("Error fetching the page:", response.status_code)
        return []

# Funkcja do załadowania przetłumaczonych tytułów z pliku
def load_translation_cache(translations_file):
    if os.path.exists(translations_file):
        with open(translations_file, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {}

# Funkcja do zapisywania przetłumaczonych tytułów do pliku
def save_translation_cache(translation_cache, translations_file):
    with open(translations_file, 'w', encoding='utf-8') as file:
        json.dump(translation_cache, file, ensure_ascii=False, indent=4)

# Funkcja do czyszczenia tytułów angielskich z niechcianymi końcówkami
def clean_english_title(title):
    # Usunięcie wzorców takich jak "(Country, English title)"
    return re.sub(r"\s*\(.*?English title\)", "", title).strip()

# Funkcja do tłumaczenia tytułów filmów na angielski za pomocą IMDb
def translate_title_to_english(polish_title, translation_cache):
    if polish_title in translation_cache:
        return translation_cache[polish_title]
    
    search_results = ia.search_movie(polish_title)
    if search_results:
        # Zakładamy, że pierwszy wynik jest najbardziej trafny
        movie = search_results[0]
        ia.update(movie)

        # Sprawdzenie, czy istnieje tytuł międzynarodowy (oryginalny/angielski)
        if 'akas' in movie:
            for aka in movie['akas']:
                if 'International' in aka or 'English' in aka:
                    english_title = aka.split('::')[-1].strip()
                    # Oczyść przetłumaczony tytuł
                    cleaned_title = clean_english_title(english_title)
                    translation_cache[polish_title] = cleaned_title  # Zapisanie do cache
                    return cleaned_title
        if 'title' in movie:
            english_title = movie['title']
            # Oczyść przetłumaczony tytuł
            cleaned_title = clean_english_title(english_title)
            translation_cache[polish_title] = cleaned_title  # Zapisanie do cache
            return cleaned_title
    
    # Jeśli nie znaleziono tłumaczenia, zwracamy oryginalny tytuł i zapisujemy do cache
    translation_cache[polish_title] = polish_title
    return polish_title

def compare_movies(watchlist, filmweb_movies, translation_cache):
    found_movies = []

    translated_titles = {}
    for filmweb_movie in filmweb_movies:
        if filmweb_movie not in translation_cache:
            translated_title = translate_title_to_english(filmweb_movie, translation_cache)
            translation_cache[filmweb_movie] = translated_title
        else:
            translated_title = translation_cache[filmweb_movie]
        
        translated_titles[filmweb_movie] = translated_title
        print(f"Translated: {filmweb_movie} -> {translated_title}")
    
    for watch_movie in watchlist:
        for filmweb_movie, translated_title in translated_titles.items():
            similarity = fuzz.ratio(watch_movie.lower(), translated_title.lower())
            if similarity > 85:
                found_movies.append((watch_movie, translated_title, similarity))
    
    return found_movies


nick = input("Podaj nazwę konta: ")

translation_cache = load_translation_cache(translations_file)

# Pobranie list filmów
letterboxd_watchlist = get_letterboxd_watchlist(nick)
filmweb_movies = get_filmweb_movies()

# Porównanie tytułów
matched_movies = compare_movies(letterboxd_watchlist, filmweb_movies, translation_cache)

# Zapisanie zaktualizowanego cache tłumaczeń do pliku
save_translation_cache(translation_cache, translations_file)

# Wyświetlenie wyników

print("\nFilmy z watchlisty, które są grane w kinach w Warszawie:")

for match in matched_movies:
    #print(f"Letterboxd: {match[0]} - Filmweb {match[1]} (Podobieństwo: {match[2]}%)")
    print(f"{match[0]} - {match[2]}%")


#end_time = time.time()
#print(f"Execution time: {end_time - start_time:.6f} seconds")
