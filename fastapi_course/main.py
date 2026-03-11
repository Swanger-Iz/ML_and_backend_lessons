from fastapi import FastAPI, HTTPException
from schemas import BANDS, Band, GenreURLChoises

app = FastAPI()


@app.get("/bands", status_code=206, response_model=list[Band])
async def bands(genre: GenreURLChoises | None = None, has_albums: bool = False) -> list[Band]:
    band_list = [Band(**b) for b in BANDS]

    if genre:
        band_list = [b for b in band_list if b.genre == genre]

    if has_albums:
        band_list = [b for b in band_list if len(b.albums) > 0]

    return band_list


@app.get("/about")
async def about() -> str:
    return "Some gachi company"


@app.get("/bands/{band_id}", status_code=206, response_model=Band)
async def get_band_id(band_id: int) -> Band:
    band = next((Band(**b) for b in BANDS if b["id"] == band_id), None)
    if band is None:
        raise HTTPException(404, "No page found")
    return band


# @app.get("/bands/genre/{genre}", status_code=206, response_model=list[Band])
# async def bands_for_genre(genre: GenreURLChoises) -> list[Band]:
#     result = [Band(**b) for b in BANDS if b["genre"] == genre]  # ...  b["genre"] == genre == b["genre"].value == genre.value
#     if len(result) == 0:
#         raise HTTPException(status_code=404, detail="No genres found")
#     return result
