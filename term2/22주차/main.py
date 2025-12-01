from fastapi import FastAPI

import models
from database import engine
from domain.question import question_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get('/')
def health_check():
    return {'message': '안녕하세요, 화성 게시판 프로젝트가 준비되었습니다!'}


app.include_router(question_router.router)


