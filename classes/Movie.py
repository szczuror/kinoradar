class Movie:
    def __init__(self, original_title, source, translated_title=None, show_dates=None, played=False):
        self.original_title = original_title
        self.translated_title = translated_title
        self.show_dates = show_dates if show_dates else []
        self.source = source
        self.played = played

    def __repr__(self):
        return f"<Tytuł: '{self.original_title}' Tytuł przetłumaczony: ({self.translated_title}) SOURCE: {self.source} data: {self.show_dates}>"
