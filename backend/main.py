
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI(title="CareerAI Navigator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://kameshwar333354.github.io"
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

CAREERS = [
    {
        "name": "Software Developer",
        "category": "Technology",
        "interests": ["coding", "technology", "problem solving"],
        "subjects": ["computer science", "math", "physics"],
        "skills": ["programming", "logic", "creativity"],
        "description": "Design, build and maintain software applications.",
        "roadmap": ["Learn Python", "Study data structures", "Learn web development", "Build projects"]
    },
    {
        "name": "Data Scientist",
        "category": "Technology",
        "interests": ["data", "mathematics", "research", "technology"],
        "subjects": ["math", "statistics", "computer science"],
        "skills": ["analysis", "programming", "problem solving"],
        "description": "Use data and statistical methods to discover useful insights.",
        "roadmap": ["Learn Python", "Study statistics", "Learn data analysis", "Build data projects"]
    },
    {
        "name": "Doctor",
        "category": "Healthcare",
        "interests": ["biology", "healthcare", "helping people", "research"],
        "subjects": ["biology", "chemistry"],
        "skills": ["communication", "observation", "empathy"],
        "description": "Diagnose illnesses and help people maintain their health.",
        "roadmap": ["Study biology and chemistry", "Prepare for medical entrance requirements", "Complete medical education", "Pursue clinical training"]
    },
    {
        "name": "Mechanical Engineer",
        "category": "Engineering",
        "interests": ["machines", "design", "technology", "problem solving"],
        "subjects": ["physics", "math"],
        "skills": ["design", "analysis", "problem solving"],
        "description": "Design and develop machines and mechanical systems.",
        "roadmap": ["Strengthen mathematics", "Study physics", "Learn engineering fundamentals", "Explore CAD and practical projects"]
    },
    {
        "name": "Civil Engineer",
        "category": "Engineering",
        "interests": ["construction", "design", "buildings", "infrastructure"],
        "subjects": ["physics", "math"],
        "skills": ["planning", "design", "problem solving"],
        "description": "Plan and develop buildings, roads and infrastructure.",
        "roadmap": ["Strengthen mathematics", "Study physics", "Learn civil engineering fundamentals", "Explore design projects"]
    },
    {
        "name": "Chartered Accountant",
        "category": "Finance",
        "interests": ["business", "finance", "accounting", "economics"],
        "subjects": ["accountancy", "math", "economics"],
        "skills": ["analysis", "attention to detail", "planning"],
        "description": "Work with accounting, auditing, taxation and financial reporting.",
        "roadmap": ["Learn accounting basics", "Understand finance", "Research CA course requirements", "Prepare for the relevant examinations"]
    },
    {
        "name": "Graphic Designer",
        "category": "Creative",
        "interests": ["art", "design", "creativity", "visual communication"],
        "subjects": ["arts", "computer science"],
        "skills": ["creativity", "visual design", "communication"],
        "description": "Create visual designs for digital and print media.",
        "roadmap": ["Learn design principles", "Explore design software", "Create a portfolio", "Complete practical projects"]
    },
    {
        "name": "Lawyer",
        "category": "Law",
        "interests": ["law", "justice", "debate", "society"],
        "subjects": ["political science", "history", "english"],
        "skills": ["communication", "research", "reasoning"],
        "description": "Study legal issues and represent or advise clients.",
        "roadmap": ["Develop reading and reasoning skills", "Research law courses", "Complete a recognised law degree", "Explore legal internships"]
    }
]


class RecommendationRequest(BaseModel):
    interests: List[str] = []
    subjects: List[str] = []
    skills: List[str] = []


class QuestionRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {
        "status": "online",
        "message": "CareerAI Navigator backend is running!"
    }


@app.get("/careers")
def get_careers():
    return {"careers": CAREERS}


@app.post("/recommend")
def recommend(request: RecommendationRequest):

    user_interests = {x.lower().strip() for x in request.interests}
    user_subjects = {x.lower().strip() for x in request.subjects}
    user_skills = {x.lower().strip() for x in request.skills}

    results = []

    for career in CAREERS:
        interest_matches = user_interests.intersection(
            career["interests"]
        )
        subject_matches = user_subjects.intersection(
            career["subjects"]
        )
        skill_matches = user_skills.intersection(
            career["skills"]
        )

        score = (
            len(interest_matches) * 3
            + len(subject_matches) * 2
            + len(skill_matches)
        )

        results.append({
            "name": career["name"],
            "category": career["category"],
            "description": career["description"],
            "score": score,
            "matched_interests": list(interest_matches),
            "matched_subjects": list(subject_matches),
            "matched_skills": list(skill_matches),
            "roadmap": career["roadmap"]
        })

    results.sort(key=lambda x: x["score"], reverse=True)

    return {
        "recommendations": results[:5],
        "notice": "These are exploratory matches, not guaranteed career outcomes."
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):

    question = request.message.lower().strip()

    if not question:
        return {"answer": "Please enter a question."}

    for career in CAREERS:
        if career["name"].lower() in question:
            return {
                "answer": (
                    f"{career['name']} is in the {career['category']} field. "
                    f"{career['description']} "
                    f"Suggested roadmap: "
                    + " → ".join(career["roadmap"])
                )
            }

    if any(word in question for word in ["roadmap", "how to start"]):
        return {
            "answer": "Choose a career that interests you, research its educational requirements, build foundational skills, complete practical projects and speak with people working in that field."
        }

    if any(word in question for word in ["engineering", "engineer"]):
        return {
            "answer": "Engineering has many branches, including computer science, mechanical, civil, electrical and chemical engineering. Compare their subjects, work and course requirements before choosing."
        }

    if any(word in question for word in ["salary", "earning", "income"]):
        return {
            "answer": "Salary varies by country, experience, qualifications, industry and employer. Check recent salary surveys and job listings for your location rather than relying on a single average."
        }

    if any(word in question for word in ["course", "degree", "college"]):
        return {
            "answer": "First identify the career you are interested in. Then check recognised courses, eligibility, entrance examinations, fees and accreditation on official college and university websites."
        }

    return {
        "answer": "I can help with career options, education pathways, skills and learning roadmaps. Try asking about a specific career, such as Software Developer, Doctor, Data Scientist or Mechanical Engineer."
    }
