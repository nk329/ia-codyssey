from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Question

router = APIRouter(
    prefix="/question",
)


@router.get("/list")
def question_list(db: Session = Depends(get_db)):
    _question_list = db.query(Question).order_by(Question.create_date.desc()).all()
    return _question_list

@router.get('/detail/{question_id}')
def question_detail(question_id: int, db: Session = Depends(get_db)):
    question = db.query(Question).filter(Question.id == question_id).first()
  
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Question not found')                      
    return question

@router.post('/create')
def question_create(_question_create: QuestionCreate, 
                    db: Session = Depends(get_db)):
    
    db_question = Question(
        subject=_question_create.subject, 
        content=_question_create.content, 
        create_date=datetime.now()
    )
    
    db.add(db_question)
    
    db.commit()
    db.refresh(db_question)
    
    return {'message': 'Question created successfully', 'id': db_question.id}
