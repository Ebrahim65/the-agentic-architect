from pydantic import BaseModel
from typing import List, Optional
import json, os
from openai import OpenAI
from dotenv import load_dotenv
 
load_dotenv()
client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.getenv("OPENROUTER_API_KEY"))
 
class WorkExperience(BaseModel):
    company: str
    title: str
    duration_months: Optional[int] = None
    responsibilities: List[str]
 
class CandidateProfile(BaseModel):
    full_name: str
    email: Optional[str] = None
    years_experience: Optional[float] = None
    skills: List[str]
    work_history: List[WorkExperience]
    highest_qualification: Optional[str] = None
    notable_achievements: List[str] = []
 
def extract_candidate_profile(cv_text: str) -> CandidateProfile:
    """
    Extract a structured candidate profile from raw CV text.
    """
    schema_json = CandidateProfile.model_json_schema()
 
    prompt = f"""You are a recruitment data specialist. Extract structured information 
from the following CV text.
 
Return ONLY a valid JSON object matching this schema exactly:
{json.dumps(schema_json, indent=2)}
 
Rules:
- Use null for missing information. Never invent details.
- Extract skills exactly as written; do not normalise or infer.
- Calculate years_experience from work history dates if possible.
 
CV TEXT:
{cv_text}"""
 
    response = client.chat.completions.create(
        model="google/gemma-4-26b-a4b-it:free",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
 
    raw = response.choices[0].message.content.strip()
    # Clean markdown code blocks if present
    if "```" in raw:
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:].strip()
 
    data = json.loads(raw)
    return CandidateProfile(**data)  # Validates with Pydantic
 
# Test
sample_cv = """
John Sithole
john.sithole@email.com | Johannesburg, SA
 
EXPERIENCE
Senior Software Developer - TechCorp (Jan 2020 – Present, 4 years)
- Led migration of monolithic system to microservices architecture
- Mentored team of 5 junior developers
- Reduced deployment time by 60% through CI/CD implementation
 
Junior Developer - StartupX (June 2018 – Dec 2019, 18 months)
- Built REST APIs using Node.js and Express
- Maintained PostgreSQL databases
 
SKILLS: Python, JavaScript, Node.js, Docker, Kubernetes, PostgreSQL, AWS
 
EDUCATION: BSc Computer Science, University of Pretoria, 2018
"""
 
if __name__ == "__main__":
    profile = extract_candidate_profile(sample_cv)
    print(profile.model_dump_json(indent=2))
