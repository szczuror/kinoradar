# 🎬 Kinoradar - Film Availability Checker

[![Python 3.7+](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Automatically checks which movies from your Letterboxd watchlist are currently playing in Warsaw cinemas using web scraping and title matching.

## 🔍 Features
- Web scraping of Warsaw cinema showtimes from Filmweb
- Fuzzy title matching with 85%+ similarity threshold 
- Automatic Polish-to-English title translation using IMDb
- Translation caching for faster repeated runs
- CSV watchlist support (Letterboxd format)

## ⚙️ Requirements
- Python 3.7+
- Required packages:
  ```bash
  requests
  beautifulsoup4
  fuzzywuzzy
  imdbpy
  ```

## 🚀 Quick Start
1. Install dependencies
```bash
 install requests beautifulsoup4 fuzzywuzzy imdbpy
```
2. Run the script
```bash
 python3 kinoradar.py
```
4. Specify the target user watchlist nickname
```bash
  Podaj nazwę konta: `nick`
```
5. Sample output
```bash
Filmy z watchlisty, które są grane w kinach w Warszawie:
Godfather - 100%
Pulp Fiction - 88%
```
Note: Percentage scores indicate title similarity (85%+ threshold). This level of similiarity usually indicates that the movie is really the one prompted, however there can be some false-positives if there are many movies with the same title.

## 🔄 Translation Mechanism
The program checks local translation cache first, and for new titles it searches IMDB database, searches for English title, normalizes it and saves in the cache. Thanks to this, the program doesn't run that slow.

## ⚠️ Problems
- Hardcoded for Warsaw (could be extended to pick a city and get information for it, or even search in specific city regions)
- Requires manual watchlist export
- Depends on filmweb and IMDB websites structure
- Possible mismatches as the translations are not perfect and sometimes not found (as they are not always in IMDB database)
- Takes long time for translating, noticeable especially when user has a long watchlist\
  
### However, all of them are solvable:)
