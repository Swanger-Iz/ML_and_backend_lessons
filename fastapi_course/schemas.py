from datetime import date
from enum import Enum

from pydantic import BaseModel, ConfigDict


class GenreURLChoises(Enum):
    POP_ROCK = "pop rock"
    BRITISH_ROCK = "british rock"
    GLAM_ROCK = "glam rock"
    HIPHOP = "hip-hop"


BANDS = [
    {
        "id": 1,
        "name": "Blink 182",
        "genre": GenreURLChoises.POP_ROCK,
        "albums": [{"title": "Album number one", "release_date": "2002-07-21"}, {"title": "Album number two", "release_date": "1999-06-17"}],
    },
    {"id": 2, "name": "Oasis", "genre": GenreURLChoises.BRITISH_ROCK, "albums": []},
    {"id": 3, "name": "Kiss", "genre": GenreURLChoises.GLAM_ROCK, "albums": []},
    {"id": 4, "name": "Wu-Tang Clan", "genre": GenreURLChoises.HIPHOP, "albums": []},
    {"id": 5, "name": "Kino", "genre": GenreURLChoises.POP_ROCK, "albums": []},
]


class Album(BaseModel):
    title: str
    release_date: date


class Band(BaseModel):
    id: int
    name: str
    genre: GenreURLChoises
    albums: list[Album] = []


result = [Band(**b) for b in BANDS if b["genre"] == GenreURLChoises.POP_ROCK and len(b["albums"]) > 0]
print(result)
