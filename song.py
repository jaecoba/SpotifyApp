class Song:
    def __init__(self, name, popularity, rank, artist):
        self.name = name
        self.popularity = popularity
        self.rank = rank
        self.artist = artist 

    def to_dict(self):
        return {
            "name": self.name,
            "popularity": self.popularity,
            "rank": self.rank,
            "artist": self.artist
        }
