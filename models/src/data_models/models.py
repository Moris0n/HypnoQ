from pydantic import BaseModel

class HypnoQueryInput(BaseModel):
    question: str

class HypnoQueryOutput(BaseModel):
    input: str
    output: str