import json
import re

import chromadb
from google import genai


def _build_eval_prompt(job_description: str, candidates: list[dict]) -> str:
    candidates_text = json.dumps(candidates, indent=2)
    return f"""You are an expert technical recruiter. Given the job description and the top 5 
candidate profiles below, evaluate each candidate.

For each candidate, provide:
- "id": the candidate's id
- "name": the candidate's name
- "title": the candidate's professional title
- "years_experience": their years of experience
- "skills": their skills array
- "previous_experience": their previous experience text
- "score": a number from 0 to 100 representing overall fit
- "pros": 1 specific sentence about their strongest qualification
- "cons": 1 specific sentence about a missing skill or weak point

Return ONLY a JSON array sorted by score descending. No markdown fences, no explanation.

Job Description:
{job_description}

Top 5 Candidate Profiles:
{candidates_text}"""


def _parse_llm_response(text: str) -> list[dict]:
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


def rank_cvs(job_description: str, api_key: str, all_candidates: list[dict]) -> list[dict]:
    """Vector-search for top 5, then RAG-evaluate them via Gemini."""
    chroma_client = chromadb.Client()

    try:
        chroma_client.delete_collection("candidates")
    except Exception:
        pass
    collection = chroma_client.create_collection(
        name="candidates",
        metadata={"hnsw:space": "cosine"},
    )

    documents = []
    ids = []
    metadatas = []
    for idx, c in enumerate(all_candidates):
        doc = f"{c.get('summary', '')} {c.get('previous_experience', '')}"
        documents.append(doc)
        ids.append(c["id"])
        metadatas.append({"name": c.get("name", ""), "index": str(idx)})

    BATCH_SIZE = 500
    for i in range(0, len(documents), BATCH_SIZE):
        collection.add(
            documents=documents[i : i + BATCH_SIZE],
            ids=ids[i : i + BATCH_SIZE],
            metadatas=metadatas[i : i + BATCH_SIZE],
        )

    results = collection.query(query_texts=[job_description], n_results=5)

    top_ids = results["ids"][0] if results["ids"] else []
    candidates_by_id = {c["id"]: c for c in all_candidates}
    top_candidates = [candidates_by_id[cid] for cid in top_ids if cid in candidates_by_id]

    if not top_candidates:
        return []

    gemini_client = genai.Client(api_key=api_key)
    prompt = _build_eval_prompt(job_description, top_candidates)
    response = gemini_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    evaluated = _parse_llm_response(response.text or "")

    for entry in evaluated:
        cid = entry.get("id", "")
        if cid in candidates_by_id:
            original = candidates_by_id[cid]
            entry.setdefault("name", original.get("name", ""))
            entry.setdefault("title", original.get("title", ""))
            entry.setdefault("years_experience", original.get("years_experience", 0))
            entry.setdefault("skills", original.get("skills", []))
            entry.setdefault("previous_experience", original.get("previous_experience", ""))

    evaluated.sort(key=lambda x: x.get("score", 0), reverse=True)
    return evaluated
