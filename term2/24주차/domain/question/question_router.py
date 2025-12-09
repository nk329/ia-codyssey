from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from domain.question.schemas import QuestionCreate, QuestionSchema
from models import Question

router = APIRouter(
    prefix='/api/question',
)


@router.get('/list', response_model=list[QuestionSchema])
def question_list(db: Session = Depends(get_db)):
    question_list_data = db.query(Question).order_by(Question.create_date.desc()).all()
    return question_list_data


@router.post('/create', response_model=QuestionSchema)
def question_create(question_create_data: QuestionCreate, db: Session = Depends(get_db)):
    db_question = Question(
        subject=question_create_data.subject,
        content=question_create_data.content,
        create_date=datetime.now(),
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

