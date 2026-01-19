from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Simple Scoring API")


class ScoreRequest(BaseModel):
    address: str
    surface: float  # m2
    rooms: Optional[int] = None


@app.get("/")
def root():
    return {"message": "Simple Scoring API. Use POST /score"}


@app.post("/score")
def score(req: ScoreRequest):
    # basic validation
    if len(req.address.strip()) < 3:
        raise HTTPException(status_code=400, detail="address is too short")

    if req.surface < 8 or req.surface > 500:
        raise HTTPException(
            status_code=400,
            detail="surface must be between 8 and 500 m2"
        )

    if req.rooms is not None and (req.rooms < 1 or req.rooms > 20):
        raise HTTPException(
            status_code=400,
            detail="rooms must be between 1 and 20"
        )

    # -----------------
    # Scoring logic
    # -----------------
    score = 50

    # surface contribution
    score += min(30, req.surface * 0.5)

    # rooms contribution
    if req.rooms is not None:
        m2_per_room = req.surface / req.rooms
        if m2_per_room >= 18:
            score += 15
        elif m2_per_room >= 12:
            score += 8
        else:
            score -= 10

    # address keyword bonus
    a = req.address.lower()
    if "metro" in a or "métro" in a or "subway" in a:
        score += 5

    # clamp score to 0–100
    score = max(0, min(100, int(round(score))))

    # -----------------
    # Grade mapping
    # -----------------
    if score >= 85:
        grade = "A"
    elif score >= 70:
        grade = "B"
    elif score >= 55:
        grade = "C"
    else:
        grade = "D"

    return {
        "score": score,
        "grade": grade
    }

