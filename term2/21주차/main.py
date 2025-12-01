from fastapi import FastAPI
import models
from domain.question import question_router

app = FastAPI()

@app.get('/')
def health_check():
    return {'message': '안녕하세요, 화성 게시판 프로젝트가 준비되었습니다!'}


app.include_router(question_router.router)
