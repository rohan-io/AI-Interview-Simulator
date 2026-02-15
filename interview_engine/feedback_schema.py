from pydantic import BaseModel, Field

class InterviewFeedback(BaseModel):
    score: int = Field(description="Score between 0 to 100")
    strengths: list[str] = Field(description="Strong points in the answer")
    weaknesses: list[str] = Field(description="Weak areas in the answer")
    improvement: str = Field(description="Suggestions for improvement")
