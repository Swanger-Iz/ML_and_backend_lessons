from datetime import date
from enum import Enum

from pydantic import BaseModel, ConfigDict, field_validator


class GenreURLChoises(Enum):
    POP_ROCK = "pop rock"
    BRITISH_ROCK = "british rock"
    GLAM_ROCK = "glam rock"
    HIPHOP = "hip-hop"


class GenreChoises(Enum):
    POP_ROCK = "Pop rock"
    BRITISH_ROCK = "British rock"
    GLAM_ROCK = "Glam rock"
    HIPHOP = "Hip-hop"
    THW = "Some genre with three words"


BANDS = [
    {
        "id": 1,
        "name": "Blink 182",
        "genre": GenreChoises.POP_ROCK,
        "albums": [{"title": "Album number one", "release_date": "2002-07-21"}, {"title": "Album number two", "release_date": "1999-06-17"}],
    },
    {"id": 2, "name": "Oasis", "genre": GenreChoises.BRITISH_ROCK, "albums": []},
    {"id": 3, "name": "Kiss", "genre": GenreChoises.GLAM_ROCK, "albums": []},
    {"id": 4, "name": "Wu-Tang Clan", "genre": GenreChoises.HIPHOP, "albums": []},
    {"id": 5, "name": "Kino", "genre": GenreChoises.POP_ROCK, "albums": []},
]


class Album(BaseModel):
    title: str
    release_date: date


class BandBase(BaseModel):
    name: str
    genre: GenreChoises
    albums: list[Album] = []


class BandCreate(BandBase):
    @field_validator("genre", mode="before")
    def title_case_genre(cls, value):
        value = value.split(" ")
        value[0] = value[0].title()
        value[1:] = [el.lower() for el in value[1:]]
        return " ".join(value)  # rock/RoCK -> Rock (pop rock -> Pop Rock)


class BandWithID(BandBase):
    id: int


result = [BandBase(**b) for b in BANDS if b["genre"] == GenreChoises.POP_ROCK and len(b["albums"]) > 0]
print(result)
