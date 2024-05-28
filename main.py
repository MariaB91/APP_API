from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import random

app = FastAPI()

security = HTTPBasic()

users = {
    "alice": "wonderland",
    "bob": "builder",
    "clementine": "mandarine"
}

class Question(BaseModel):
    question: str
    subject: str
    correct: List[str]
    use: str
    responseA: str
    responseB: str
    responseC: str
    responseD: Optional[str] = None

class QuestionRequest(BaseModel):
    use: str
    subjects: List[str]
    count: int

class NewQuestion(BaseModel):
    question: str
    subject: str
    correct: List[str]
    use: str
    responseA: str
    responseB: str
    responseC: str
    responseD: Optional[str] = None

def authenticate_user(credentials: HTTPBasicCredentials):
    if credentials.username in users and users[credentials.username] == credentials.password:
        return credentials.username
    return None

def load_questions(filepath: str):
    return pd.read_csv(filepath)

questions_df = load_questions("questions.csv")

@app.get("/healthcheck")
async def health_check():
    return {"status": "API is running"}

@app.get("/questions", response_model=List[Question])
async def get_questions(
    use: str, 
    subjects: List[str], 
    count: int, 
    credentials: HTTPBasicCredentials = Depends(security)
):
    user = authenticate_user(credentials)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    filtered_df = questions_df[
        (questions_df['use'] == use) & 
        (questions_df['subject'].isin(subjects))
    ]

    if filtered_df.empty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No questions found for the given criteria"
        )

    questions = filtered_df.sample(n=count).to_dict(orient='records')
    return questions

@app.post("/questions")
async def create_question(
    new_question: NewQuestion, 
    credentials: HTTPBasicCredentials = Depends(security)
):
    user = authenticate_user(credentials)
    if user != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )

    new_data = new_question.dict()
    new_df = pd.DataFrame([new_data])
    global questions_df
    questions_df = pd.concat([questions_df, new_df], ignore_index=True)
    questions_df.to_csv("questions.csv", index=False)
    return {"message": "Question created successfully"}
