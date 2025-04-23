class Movie:
    title: str
    year: int
    translated_title: str = None
    nearest_screening_year: int
    nearest_screening_hour: int
    source: str

    def __init__(self, title, year):
        self.title = title
        self.year = year
        self.translated_title = None
        self.source = None
