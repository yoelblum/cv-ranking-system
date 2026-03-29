from fastapi import APIRouter, Header, HTTPException

from app.config import get_api_key
from app.database import wipe_and_insert
from app.models import GenerateResponse, JobDescriptionRequest
from app.services.generator import generate_cvs

router = APIRouter(prefix="/api")


@router.post("/generate-cvs", response_model=GenerateResponse)
async def generate(body: JobDescriptionRequest, x_api_key: str | None = Header(None)):
    try:
        api_key = get_api_key(x_api_key)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    try:
        candidates = await generate_cvs(body.job_description, api_key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"CV generation failed: {e}")

    count = wipe_and_insert(candidates)
    return GenerateResponse(
        message=f"Successfully generated and stored {count} candidate CVs.",
        count=count,
    )
