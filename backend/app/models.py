from pydantic import BaseModel


class JobDescriptionRequest(BaseModel):
    job_description: str


class GenerateResponse(BaseModel):
    message: str
    count: int


class RankedCandidate(BaseModel):
    id: str
    name: str
    title: str
    years_experience: int
    skills: list[str]
    previous_experience: str
    score: int
    pros: str
    cons: str


class RankResponse(BaseModel):
    candidates: list[RankedCandidate]
