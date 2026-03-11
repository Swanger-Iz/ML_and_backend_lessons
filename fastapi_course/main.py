from fastapi import FastAPI, HTTPException
from schemas import BANDS, BandBase, BandCreate, BandWithID, GenreChoises

app = FastAPI()


@app.get("/bands", status_code=206, response_model=list[BandWithID])
async def bands(genre: GenreChoises | None = None, has_albums: bool = False) -> list[BandWithID]:
    band_list = [BandWithID(**b) for b in BANDS]

    if genre:
        band_list = [b for b in band_list if b.genre.lower() == genre]

    if has_albums:
        band_list = [b for b in band_list if len(b.albums) > 0]

    return band_list


@app.get("/about")
async def about() -> str:
    return "Some gachi company"


@app.get("/bands/{band_id}", status_code=206, response_model=BandWithID)
async def get_band_id(band_id: int) -> BandWithID:
    band = next((BandWithID(**b) for b in BANDS if b["id"] == band_id), None)
    if band is None:
        raise HTTPException(404, "No page found")
    return band


@app.post("/bands", status_code=200, response_model=BandWithID)
async def create_band(band_data: BandCreate) -> BandWithID:
    id = BANDS[-1]["id"] + 1
    band = BandWithID(id=id, **band_data.model_dump()).model_dump()
    BANDS.append(band)
    return band


# @app.get("/bands/genre/{genre}", status_code=206, response_model=list[Band])
# async def bands_for_genre(genre: GenreURLChoises) -> list[Band]:
#     result = [Band(**b) for b in BANDS if b["genre"] == genre]  # ...  b["genre"] == genre == b["genre"].value == genre.value
#     if len(result) == 0:
#         raise HTTPException(status_code=404, detail="No genres found")
#     return result
