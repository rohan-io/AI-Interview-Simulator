import os
import json
from groq import Groq

# NEW IMPORTS (LangChain evaluator)
from interview_engine.evaluator import evaluate_answer
from llm.llm_config import get_llm


# ==============================
# EVALUATE ANSWERS (UPDATED)
# ==============================

def evaluate_answers(questions_answers):

    llm = get_llm()   # Initialize ONCE

    feedback_list = []

    for qa in questions_answers:

        feedback = evaluate_answer(
            llm,
            qa["question"],
            qa["answer"]
        )

        feedback_list.append({
            "score": feedback.score,
            "strengths": feedback.strengths,
            "weaknesses": feedback.weaknesses,
            "improvement": feedback.improvement
        })

    return feedback_list


# ==============================
# GENERATE QUESTIONS (KEEP SAME)
# ==============================

def generate_questions(role, difficulty, tech_stack):

    client = Groq(
        api_key=os.getenv("GROQ_API_KEY")
    )

    prompt = f"""
You are a professional technical interviewer.

Generate 5 REALISTIC interview questions for:

Role: {role}
Technology: {tech_stack}
Difficulty: {difficulty}

Rules:
- Questions must be based on the specific technology
- Ask practical real-world interview questions
- Avoid theoretical textbook definitions
- Focus on problem-solving
- Questions should match the difficulty level

Return ONLY JSON like:

[
  "question 1",
  "question 2",
  "question 3",
  "question 4",
  "question 5"
]
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    output = response.choices[0].message.content

    try:
        return json.loads(output)
    except:
        return []
