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
    if difficulty.lower() == "easy":
        difficulty_rules = """
Generate:
- 4 short concept-based questions
- 1 simple real-world scenario question

Questions should be:
- Definition based
- Concept understanding based
- Beginner level
- NOT lengthy
- Direct questions like:
    • What is ___?
    • Explain ___
    • What do you mean by ___?
"""

    elif difficulty.lower() == "medium":
        difficulty_rules = """
Generate:
- 3 concept-based questions
- 2 practical real-world scenario questions

Questions should:
- Test application of concepts
- Include implementation understanding
- Be moderately challenging
"""

    elif difficulty.lower() == "hard":
        difficulty_rules = """
Generate:
- 1 concept-based question
- 4 complex real-world scenario/problem-solving questions

Questions should:
- Be implementation heavy
- Ask "How would you design / optimize / handle"
- Require deep technical understanding
"""

    prompt = f"""
You are a professional technical interviewer.

Generate 5 interview questions for:

Role: {role}
Technology: {tech_stack}
Difficulty: {difficulty}

IMPORTANT:

{difficulty_rules}

Rules:
- Questions must be based on the selected technology
- Avoid theoretical textbook language
- Match the difficulty level strictly
- DO NOT make all questions scenario based
- Easy should be short
- Hard should involve design/problem solving

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
