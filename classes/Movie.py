from dataclasses import dataclass

@dataclass
class Movie:
    title: str
    year: int
    source: str
    translated_title: str
    nearest_screening: str

# jeśli nie uda przetłumaczyć się tytułu filmu, to zostanie użyta nazwa oryginalna

    def __post_init__(self):
        if self.translated_title is None:
            self.translated_title = self.title

