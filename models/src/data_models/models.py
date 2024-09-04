from pydantic import BaseModel

class HypnoQueryInput(BaseModel):
    question: str

class HypnoQueryOutput(BaseModel):
    input: str
    output: str

class FeedbackInput(BaseModel):
    question: str
    answer: str
    helpful: bool

class FeedbackOutput(BaseModel):
    message: str
    original_question: str = None  # Optional field, only included if feedback is not helpful
