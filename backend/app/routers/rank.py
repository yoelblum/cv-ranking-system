from fastapi import APIRouter, Header, HTTPException

from app.config import get_api_key
from app.database import get_all_candidates
from app.models import JobDescriptionRequest, RankResponse
from app.services.ranker import rank_cvs

router = APIRouter(prefix="/api")


@router.post("/rank-cvs", response_model=RankResponse)
async def rank(body: JobDescriptionRequest, x_api_key: str | None = Header(None)):
    try:
        api_key = get_api_key(x_api_key)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    all_candidates = get_all_candidates()
    if not all_candidates:
        raise HTTPException(
            status_code=400,
            detail="No candidates in database. Run Generate first.",
        )

    try:
        ranked = rank_cvs(body.job_description, api_key, all_candidates)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ranking failed: {e}")

    return RankResponse(candidates=ranked)
