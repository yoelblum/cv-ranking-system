import asyncio
import json
import random
import re
import uuid

from faker import Faker
from google import genai

fake = Faker()

SYNONYM_MAP: dict[str, list[str]] = {
    "Led": ["Managed", "Spearheaded", "Directed", "Oversaw", "Headed"],
    "Managed": ["Led", "Supervised", "Coordinated", "Oversaw", "Directed"],
    "Developed": ["Built", "Engineered", "Created", "Designed", "Implemented"],
    "Built": ["Developed", "Constructed", "Engineered", "Created", "Assembled"],
    "Implemented": ["Deployed", "Executed", "Rolled out", "Introduced", "Established"],
    "Designed": ["Architected", "Crafted", "Planned", "Devised", "Conceptualized"],
    "Improved": ["Enhanced", "Optimized", "Upgraded", "Refined", "Strengthened"],
    "Optimized": ["Improved", "Streamlined", "Fine-tuned", "Enhanced", "Refined"],
    "extensive": ["solid", "deep", "broad", "comprehensive", "strong"],
    "strong": ["solid", "robust", "proven", "excellent", "deep"],
    "experienced": ["skilled", "proficient", "seasoned", "adept", "accomplished"],
    "proficient": ["skilled", "experienced", "adept", "competent", "well-versed"],
}


def _synonym_swap(text: str) -> str:
    """Apply light synonym swaps to a piece of text (case-insensitive)."""
    for word, replacements in SYNONYM_MAP.items():
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        if pattern.search(text) and random.random() < 0.4:
            text = pattern.sub(random.choice(replacements), text, count=1)
    return text


def _vary_skills(skills: list[str]) -> list[str]:
    """Shuffle and optionally drop 0-1 skills."""
    varied = list(skills)
    random.shuffle(varied)
    if len(varied) > 2 and random.random() < 0.5:
        varied.pop(random.randint(0, len(varied) - 1))
    return varied


def _build_prompt(job_description: str) -> str:
    return f"""You are a realistic CV dataset generator. Given the following job description, 
generate a JSON array of exactly 20 candidate CVs. 

IMPORTANT RULES:
- Create a realistic MIX: ~8 strong matches, ~7 partial matches, ~5 wildcards/poor fits.
- Tailor candidates to the job description's location and industry. If the JD mentions a 
  specific country or city, generate candidates with work experience and companies from that region.
- Each CV must have these exact fields:
  - "id": a unique string identifier (e.g. "cv-1", "cv-2", ...)
  - "title": the candidate's professional title
  - "years_experience": integer years of experience
  - "skills": an array of 4-8 technical skills as strings
  - "summary": a 2-3 sentence professional summary
  - "previous_experience": 1-3 sentences describing past roles, companies worked at, and key projects

Return ONLY the JSON array. No markdown fences, no explanation, no extra text.

Job Description:
{job_description}"""


def _parse_llm_response(text: str) -> list[dict]:
    """Extract a JSON array from the LLM response, tolerating markdown fences."""
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    try:
        data = json.loads(cleaned)
        if isinstance(data, list):
            return data
    except json.JSONDecodeError:
        match = re.search(r"\[.*\]", cleaned, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass
    return []


async def _call_gemini(client: genai.Client, prompt: str) -> list[dict]:
    response = await client.aio.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    return _parse_llm_response(response.text or "")


def _multiply_archetypes(archetypes: list[dict], clones_per: int = 20) -> list[dict]:
    """Clone each archetype into `clones_per` unique candidates using Faker + random variation."""
    all_candidates = []
    for archetype in archetypes:
        for _ in range(clones_per):
            candidate = {
                "id": str(uuid.uuid4()),
                "name": fake.name(),
                "email": fake.email(),
                "phone": fake.phone_number(),
                "title": archetype.get("title", ""),
                "years_experience": max(0, archetype.get("years_experience", 3) + random.randint(-3, 3)),
                "skills": _vary_skills(archetype.get("skills", [])),
                "summary": _synonym_swap(archetype.get("summary", "")),
                "previous_experience": _synonym_swap(archetype.get("previous_experience", "")),
            }
            all_candidates.append(candidate)
    return all_candidates


async def generate_cvs(job_description: str, api_key: str) -> list[dict]:
    """Seed 60 archetypes via 3 concurrent Gemini calls, then multiply to 600."""
    client = genai.Client(api_key=api_key)
    prompt = _build_prompt(job_description)

    batches = await asyncio.gather(
        _call_gemini(client, prompt),
        _call_gemini(client, prompt),
        _call_gemini(client, prompt),
    )

    archetypes: list[dict] = [cv for batch in batches for cv in batch]

    if not archetypes:
        raise ValueError("LLM returned no valid CV data. Check your API key and try again.")

    candidates = _multiply_archetypes(archetypes, clones_per=10)
    return candidates
