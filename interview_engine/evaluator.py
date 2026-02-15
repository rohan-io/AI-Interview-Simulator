from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from interview_engine.feedback_schema import InterviewFeedback


def evaluate_answer(llm, question, answer):

    parser = PydanticOutputParser(
        pydantic_object=InterviewFeedback
    )

    prompt = ChatPromptTemplate.from_template("""
    You are a strict technical interviewer.

    Evaluate the candidate's answer.

    IMPORTANT:
    Keep the feedback SHORT and UI-friendly.

    Follow these rules strictly:
    - Score must be between 0 to 100
    - Strengths must be max 2 short bullet points
    - Weaknesses must be max 2 short bullet points
    - Improvement must be only 1 actionable suggestion
    - DO NOT write paragraphs
    - Each point must be less than 10 words
    - Be concise

    Return ONLY in required JSON format.

    {format_instructions}

    Question:
    {question}

    Answer:
    {answer}
    """)


    # LCEL chain with auto-retry parser
    chain = prompt | llm | parser.with_retry()

    feedback = chain.invoke({
        "question": question,
        "answer": answer,
        "format_instructions": parser.get_format_instructions()
    })

    return feedback
