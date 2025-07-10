# Kinoradar

Skrypt Python sprawdzający, które filmy z Twojej watchlisty na Letterboxd są obecnie wyświetlane w kinach w Warszawie. Automatycznie porównuje Twoją listę z aktualnym repertuarem kin z Filmwebu i wyświetla pasujące tytuły.

## Jak to działa

1. Pobiera Twoją watchlistę z Letterboxd
2. Sprawdza aktualny repertuar kin w Warszawie
3. Tłumaczy polskie tytuły na angielskie przy użyciu danych z IMDb
4. Porównuje tytuły z użyciem fuzzy matching
5. Wyświetla pasujące filmy z procentowym podobieństwem

## Wymagania

- Python 3.7+
- Biblioteki:
  ```
  requests
  beautifulsoup4
  imdbpy
  fuzzywuzzy
  python-Levenshtein
  ```

## Instalacja i użycie

1. Sklonuj repozytorium:
```bash
git clone https://github.com/szczuror/kinoradar.git
cd kinoradar
```

2. Zainstaluj zależności:
```bash
pip install requests beautifulsoup4 imdbpy fuzzywuzzy python-Levenshtein
```

3. Uruchom skrypt:
```bash
python kinoradar.py
```

4. Podaj swoją nazwę użytkownika Letterboxd po wyświetleniu komunikatu

## Przykładowy output
```
Podaj nazwę konta: user

Tłumaczenie: Barbie -> Barbie
Tłumaczenie: Anatomia upadku -> Anatomy of a Fall

Filmy z watchlisty, które są grane w kinach w Warszawie:
Barbie - 100%
Anatomy of a Fall - 92%
```

## Uwagi

- Plik z tłumaczeniami (`translations.json`) tworzy się automatycznie
- Domyślny próg dopasowania to 85%
- Skrypt aktualnie wspiera tylko Warszawę (relatywnie proste do zmiany w razie potrzeby)

## Restrukturyzacja projektu w trakcie, w planach:

- Filtrowanie kin po lokalizacji
- Wyświetlanie dokładnych terminów seansów
- Ułatwienie dodawania repertuarów nowych kin, czyli chociażby zmiany lokalizacji
- Uniezależnienie się od konkretnych stron i stworzenie oddzielnych fetcherów dla każdego z kin

## Licencja

Ten projekt jest dostępny na licencji MIT
