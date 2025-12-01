from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from domain.question.schemas import QuestionSchema
from models import Question

router = APIRouter(
    prefix='/api/question',
)


@router.get('/list', response_model=list[QuestionSchema])
def question_list(db: Session = Depends(get_db)):
    question_list_data = db.query(Question).order_by(Question.create_date.desc()).all()
    return question_list_data

